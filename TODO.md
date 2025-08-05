# TODO: Optimisations for Noise Removal & Curve Fitting Widgets

## General Observations
- **Heavy use of Python for pixel-wise operations**: Pixel-wise and nested-loop operations in Python are inherently slow due to interpreter overhead. The best way to optimise is to refactor these routines to use NumPy vectorisation, which leverages compiled C code under the hood. For even greater speed, consider Cython or Numba to JIT-compile critical sections. For extremely large datasets, chunking and memory-mapping can help avoid memory bottlenecks.
- **Multiprocessing is used for curve fitting**: Multiprocessing is effective for CPU-bound tasks, but Python's multiprocessing has overhead for process creation and inter-process communication. For small datasets, a single-threaded approach may be faster. For large datasets, consider using joblib for more flexible parallelism, or Dask for distributed computation. Batching curve fits and using shared memory arrays can reduce overhead.

## Noise Removal (`core/noiseremoval.py`)
**Background subtraction, hot pixel removal, thresholding, masking**:
  - **Refactor to Cython/Numba/NumPy**: Audit the underlying dataset methods. If they use Python loops, rewrite them using NumPy for vectorised operations. For more complex logic, use Numba's `@jit` decorator or Cython for compiled speed. This can yield 10-100x speedups for pixel-wise routines.
  - **Chunking**: Implement adaptive chunking based on available RAM and CPU cores. Use `psutil` to detect system resources and auto-tune chunk sizes. For distributed systems, Dask arrays can handle chunking and parallelism transparently.
  - **Kernel size for hot pixel removal**: Benchmark different kernel sizes on representative datasets. Use a configuration option or auto-tune based on image statistics (e.g., noise level, image size).
  - **Masking**: If masks are sparse, use `scipy.sparse` arrays to reduce memory and computation. For binary masks, use bitwise operations for speed.

## Curve Fitting (`core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`)
**Multiprocessing Pool**: Uses all but one CPU for fitting. Good, but:
  - **Pool overhead**: Profile the time spent in process creation and data transfer. For small jobs, use a single-threaded fallback. For large jobs, batch curve fits and use shared memory (e.g., `multiprocessing.Array` or `numpy.memmap`).
  - **Data transfer**: Minimise the amount of data sent to worker processes. Use shared memory or memory-mapped files for large arrays. Consider using Dask for out-of-core and distributed computation.
  - **Progress bar (tqdm)**: When using multiprocessing, update the progress bar from the main process only, or use a shared counter. Excessive logging or progress updates can slow down parallel code.
**Fit methods**: Benchmark all available algorithms (`trf`, `dogbox`, `lm`) on typical datasets. Implement an auto-selection routine that chooses the best method based on data size, sparsity, and problem type. Allow users to override if needed.
**Widget logic**:
  - **UI blocking**: Move curve fitting to a background thread or process using `QThread` or `concurrent.futures`. Use signals/slots to update the UI asynchronously. Show progress and allow cancellation.
  - **Abort button**: Implement a cancellation token or flag that worker threads/processes check periodically. For multiprocessing, use a shared variable or terminate the pool gracefully.
  - **Residuals calculation**: Replace `numpy.sqrt(numpy.subtract(...)) ** 2` with `numpy.abs(...)` for speed and clarity, unless true RMS error is needed.
  - **Plotting**: Downsample large images/curves before plotting. Use `skimage.transform.resize` or similar. For interactive plots, consider lazy loading or progressive rendering.

## Other Potential Improvements
**NumPy vectorisation**: Systematically review all pixel-wise and nested-loop code. Replace with NumPy operations wherever possible. For example, use `numpy.where`, `numpy.sum`, and broadcasting instead of explicit loops.
**Cython/Numba**: Use profiling tools (`cProfile`, `line_profiler`) to identify slow functions. Rewrite these in Cython for compiled speed, or use Numba's `@jit` for easy JIT compilation. Test for correctness and speedup.
**Memory usage**: Use memory profiling tools (`memory_profiler`, `tracemalloc`) to track memory usage. For large arrays, use `numpy.memmap` or Dask arrays to avoid loading everything into RAM. Free unused memory promptly.
**I/O bottlenecks**: For large datasets, use memory-mapped files (`numpy.memmap`) or asynchronous I/O (`aiofiles`, `asyncio`). Consider chunked reading and writing. For HDF5, use `h5py` with chunking and compression.
**Testing and benchmarking**: Add unit tests and benchmarks for all critical routines. Use `pytest-benchmark` or custom timing scripts. Track performance over time and after each optimisation.

## Action Items
1. **Profile noise removal and curve fitting functions to identify bottlenecks.**
   - Use `cProfile`, `line_profiler`, and `memory_profiler` to find slow and memory-intensive routines. Focus on pixel-wise loops, curve fitting, and I/O.
2. **Benchmark different fit methods and select optimal default based on data/problem size.**
   - Create a benchmarking suite with representative datasets. Test all fit algorithms and record speed/accuracy. Implement logic to auto-select the best method, with user override.
3. **Implement proper chunking and batching for large datasets.**
   - Use `psutil` to detect available RAM/CPU and auto-tune chunk sizes. For distributed systems, use Dask arrays. For GPU, batch fits to maximise throughput.
4. **Add support for background processing and UI responsiveness in widgets.**
   - Move heavy computation to background threads/processes. Use Qt's `QThread` or Python's `concurrent.futures`. Update UI via signals/slots. Show progress and allow cancellation.
5. **Fix abort/cancellation logic for long-running operations.**
   - Implement cancellation tokens/flags. For multiprocessing, use shared variables or terminate pools gracefully. For GPU, use asynchronous kernels and check for cancellation.
6. **Consider Cython/Numba for core pixel-wise routines.**
   - Profile and rewrite slow routines in Cython or Numba. Test for correctness and speedup. Document changes and maintainability.
7. **Document and auto-tune parameters (e.g., chunk size, kernel size).**
   - Add documentation for all tunable parameters. Implement auto-tuning based on dataset size and system resources. Allow user override.
8. **Optimise residuals calculation and plotting routines.**
   - Use vectorised NumPy operations for residuals. Downsample data for plotting. For interactive plots, use lazy loading or progressive rendering.

## GPU Acceleration for Curve Fitting

- **CUDA/ROCm Integration**: Use libraries such as CuPy (NVIDIA CUDA) or ROCm's HIP (AMD) to accelerate NumPy-like operations on the GPU. For curve fitting, port critical routines to GPU using CuPy or PyTorch. For custom kernels, write CUDA C or HIP code and wrap with Python.
- **Batching Fits**: GPUs excel at parallel batch processing. Reshape data so that many curves are fit in parallel. Use GPU libraries for least-squares fitting, e.g., CuPy's `cupy.linalg.lstsq` or PyTorch's optimisers.
- **Resource Detection**: Use `cupy.cuda.runtime.getDeviceCount()` or `torch.cuda.device_count()` to detect available GPUs. For ROCm, use `hip` or `rocm-smi` tools. Query device properties to select the best GPU for the job.
- **Fallback Logic**: If no GPU is available, fall back to CPU (NumPy/Numba/Cython). Allow user to select preferred device.
- **Data Transfer**: Minimise host-device transfers. Keep data on GPU as much as possible. Use pinned memory for fast transfers.
- **Error Handling**: Gracefully handle GPU errors and out-of-memory conditions. Log and notify the user.

## Resource Assessment Widget

- **Widget Design**: Create a widget that scans available system resources (CPU cores, RAM, GPUs). Display detected devices and their properties (e.g., GPU model, VRAM, CUDA/ROCm version).
- **Best Use Suggestion**: Based on dataset size and available resources, suggest the optimal processing mode (CPU single-threaded, CPU multi-threaded, GPU batch, distributed/Dask). Provide recommendations and allow user override.
- **Integration**: On widget startup, run resource detection routines. Use `psutil` for CPU/RAM, `cupy`/`torch` for GPU. Display results in a user-friendly format.
- **Advanced Options**: Allow users to select device, set chunk/batch size, and enable/disable GPU acceleration. Warn if resources are insufficient for the requested operation.
- **Extensibility**: Design widget to support future hardware (e.g., multi-GPU, cloud resources).

---

# TODO: Optimisations for Noise Removal & Curve Fitting Widgets

- **Resource Detection**: Use `cupy.cuda.runtime.getDeviceCount()` or `torch.cuda.device_count()` to detect available GPUs. For ROCm, use `hip` or `rocm-smi` tools. Query device properties to select the best GPU for the job.
- **Fallback Logic**: If no GPU is available, fall back to CPU (NumPy/Numba/Cython). Allow user to select preferred device.
- **Data Transfer**: Minimise host-device transfers. Keep data on GPU as much as possible. Use pinned memory for fast transfers.
- **Error Handling**: Gracefully handle GPU errors and out-of-memory conditions. Log and notify the user.

## Resource Assessment Widget

- **Widget Design**: Create a widget that scans available system resources (CPU cores, RAM, GPUs). Display detected devices and their properties (e.g., GPU model, VRAM, CUDA/ROCm version).
- **Best Use Suggestion**: Based on dataset size and available resources, suggest the optimal processing mode (CPU single-threaded, CPU multi-threaded, GPU batch, distributed/Dask). Provide recommendations and allow user override.
- **Integration**: On widget startup, run resource detection routines. Use `psutil` for CPU/RAM, `cupy`/`torch` for GPU. Display results in a user-friendly format.
- **Advanced Options**: Allow users to select device, set chunk/batch size, and enable/disable GPU acceleration. Warn if resources are insufficient for the requested operation.
- **Extensibility**: Design widget to support future hardware (e.g., multi-GPU, cloud resources).

---

## Optimisation Steps Checklist

### General Observations

- [ ] **Refactor pixel-wise and nested-loop operations to use NumPy vectorisation:**
    - **Action:** Identify functions in the codebase that perform pixel-wise operations using Python loops (e.g., iterating through image pixels).
    - **Implementation:** Replace these loops with equivalent NumPy operations using functions like `numpy.vectorize`, `numpy.where`, `numpy.sum`, and broadcasting.
    - **Example:** Replace `for i in range(image.shape[0]): for j in range(image.shape[1]): ...` with `numpy.where(condition, image1, image2)`.
    - **Files to Examine:** All files, focusing on image processing functions.

- [ ] **Profile and identify bottlenecks for interpreter overhead:**
    - **Action:** Use profiling tools to identify functions with significant interpreter overhead.
    - **Implementation:** Use `cProfile` or `line_profiler` to profile the code during typical use cases.
    - **Command:** `python -m cProfile -o profile_output.prof your_script.py`
    - **Analysis:** Analyze the output to identify the slowest functions.

- [ ] **Consider Cython or Numba for JIT-compiling critical sections:**
    - **Action:** Rewrite identified bottleneck functions in Cython or use Numba's `@jit` decorator.
    - **Implementation:**
        - **Cython:** Create `.pyx` files for slow functions, compile them to C code, and then to Python extensions.
        - **Numba:** Add `@jit` decorator to functions that can benefit from JIT compilation.
    - **Files to Examine:** Files identified in the profiling step.

- [ ] **Implement chunking and memory-mapping for very large datasets:**
    - **Action:** Modify code to process large datasets in chunks instead of loading the entire dataset into memory.
    - **Implementation:**
        - Use `numpy.memmap` to create memory-mapped arrays.
        - Implement chunking logic to process data in smaller blocks.
    - **Files to Examine:** Data loading and processing functions.

- [ ] **Evaluate multiprocessing overhead and consider joblib/Dask for parallelism:**
    - **Action:** Profile the multiprocessing implementation to measure overhead.
    - **Implementation:**
        - Use `timeit` to measure the execution time of parallel and serial versions.
        - If overhead is significant, consider using `joblib` for simpler parallelism or `Dask` for distributed computation.
    - **Files to Examine:** Multiprocessing-related files.

- [ ] **Batch curve fits and use shared memory arrays to reduce overhead:**
    - **Action:** Batch multiple curve fitting operations into a single process and use shared memory to reduce data transfer overhead.
    - **Implementation:**
        - Group multiple curve fitting tasks into batches.
        - Use `multiprocessing.Array` or `numpy.memmap` for shared memory.
    - **Files to Examine:** Curve fitting functions.

### Noise Removal (`core/noiseremoval.py`)

- [ ] **Audit dataset methods for Python loops and refactor to NumPy:**
    - **Action:** Examine the dataset methods used in `core/noiseremoval.py` for Python loops.
    - **Implementation:** Replace loops with NumPy operations.
    - **Files to Examine:** `core/noiseremoval.py` and related dataset files.

- [ ] **Use Numba's `@jit` or Cython for complex logic:**
    - **Action:** Apply Numba's `@jit` decorator or rewrite complex logic in Cython for speedup.
    - **Implementation:**
        - Add `@jit` to functions in `core/noiseremoval.py`.
        - Rewrite functions in Cython if necessary.
    - **Files to Examine:** `core/noiseremoval.py`.

- [ ] **Implement adaptive chunking using `psutil` for resource detection:**
    - **Action:** Implement adaptive chunking based on available RAM and CPU cores.
    - **Implementation:**
        - Use `psutil` to detect system resources.
        - Adjust chunk sizes based on available resources.
    - **Files to Examine:** `core/noiseremoval.py`.

- [ ] **Benchmark kernel sizes for hot pixel removal and auto-tune:**
    - **Action:** Test different kernel sizes on representative datasets and auto-tune based on image statistics.
    - **Implementation:**
        - Implement a benchmarking routine to test different kernel sizes.
        - Auto-tune based on image statistics (e.g., noise level, image size).
    - **Files to Examine:** `core/noiseremoval.py`.

- [ ] **Use `scipy.sparse` arrays for sparse masks:**
    - **Action:** If masks are sparse, use `scipy.sparse` arrays to reduce memory and computation.
    - **Implementation:**
        - Replace dense arrays with `scipy.sparse` arrays where appropriate.
    - **Files to Examine:** `core/noiseremoval.py`.

- [ ] **Use bitwise operations for binary masks:**
    - **Action:** Use bitwise operations for binary masks to improve speed.
    - **Implementation:**
        - Replace logical operations with bitwise operations (e.g., `&`, `|`, `^`).
    - **Files to Examine:** `core/noiseremoval.py`.

### Curve Fitting (`core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`)

- [ ] **Profile process creation and data transfer overhead in multiprocessing:**
    - **Action:** Measure the time spent in process creation and data transfer.
    - **Implementation:**
        - Use `timeit` to measure the overhead.
        - Use shared memory or memory-mapped files for large arrays.
    - **Files to Examine:** `core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Use single-threaded fallback for small jobs:**
    - **Action:** Implement a single-threaded fallback for small datasets to avoid multiprocessing overhead.
    - **Implementation:**
        - Check the size of the dataset.
        - If the size is below a threshold, use a single-threaded implementation.
    - **Files to Examine:** `core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Minimise data sent to worker processes:**
    - **Action:** Reduce the amount of data sent to worker processes by using shared memory or memory-mapped files.
    - **Implementation:**
        - Use `multiprocessing.Array` or `numpy.memmap` for large arrays.
    - **Files to Examine:** `core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Update progress bar from the main process only:**
    - **Action:** Ensure that the progress bar is updated from the main process only to avoid slowing down parallel code.
    - **Implementation:**
        - Use a shared counter and update the progress bar from the main process.
    - **Files to Examine:** `core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Benchmark all available fit algorithms:**
    - **Action:** Benchmark all available algorithms (`trf`, `dogbox`, `lm`) on typical datasets.
    - **Implementation:**
        - Implement a benchmarking routine to test all algorithms.
        - Record the execution time for each algorithm.
    - **Files to Examine:** `core/rocking_curves.py`.

- [ ] **Implement auto-selection routine for fit methods:**
    - **Action:** Implement an auto-selection routine that chooses the best method based on data size, sparsity, and problem type.
    - **Implementation:**
        - Analyse the data size, sparsity, and problem type.
        - Select the best algorithm based on the analysis.
    - **Files to Examine:** `core/rocking_curves.py`.

- [ ] **Move curve fitting to a background thread or process:**
    - **Action:** Move curve fitting to a background thread or process using `QThread` or `concurrent.futures`.
    - **Implementation:**
        - Use `QThread` or `concurrent.futures` to run curve fitting in the background.
        - Use signals/slots to update the UI asynchronously.
    - **Files to Examine:** `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Implement a cancellation token or flag:**
    - **Action:** Implement a cancellation token or flag that worker threads/processes check periodically.
    - **Implementation:**
        - Use a shared variable or terminate the pool gracefully.
    - **Files to Examine:** `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Replace `numpy.sqrt(numpy.subtract(...)) ** 2` with `numpy.abs(...)`:**
    - **Action:** Replace the expression with `numpy.abs(...)` for speed and clarity.
    - **Implementation:**
        - Modify the code to use `numpy.abs(...)`.
    - **Files to Examine:** `core/rocking_curves.py`, `gui/rocking_curves/rockingCurvesWidget.py`.

- [ ] **Downsample large images/curves before plotting:**
    - **Action:** Downsample large images/curves before plotting to improve performance.
    - **Implementation:**
        - Use `skimage.transform.resize` or similar.
    - **Files to Examine:** `gui/rocking_curves/rockingCurvesWidget.py`.

### Other Potential Improvements

- [ ] **Systematically review all pixel-wise and nested-loop code:**
    - **Action:** Review all code for pixel-wise and nested-loop operations.
    - **Implementation:**
        - Replace with NumPy operations wherever possible.
    - **Files to Examine:** All files.

- [ ] **Use profiling tools to identify slow functions:**
    - **Action:** Use profiling tools (`cProfile`, `line_profiler`) to identify slow functions.
    - **Implementation:**
        - Rewrite these in Cython for compiled speed, or use Numba's `@jit` for easy JIT compilation.
    - **Files to Examine:** All files.

- [ ] **Use memory profiling tools to track memory usage:**
    - **Action:** Use memory profiling tools (`memory_profiler`, `tracemalloc`) to track memory usage.
    - **Implementation:**
        - For large arrays, use `numpy.memmap` or Dask arrays to avoid loading everything into RAM.
    - **Files to Examine:** All files.

- [ ] **Use memory-mapped files or asynchronous I/O:**
    - **Action:** For large datasets, use memory-mapped files (`numpy.memmap`) or asynchronous I/O (`aiofiles`, `asyncio`).
    - **Implementation:**
        - Consider chunked reading and writing.
        - For HDF5, use `h5py` with chunking and compression.
    - **Files to Examine:** All files.

### GPU Acceleration (CUDA/ROCm)

- [ ] **Resource Detection:**
    - **Action:** Use `cupy.cuda.runtime.getDeviceCount()` or `torch.cuda.device_count()` to detect available GPUs. For ROCm, use `hip` or `rocm-smi` tools.
    - **Implementation:**
        - Implement resource detection routines.
    - **Files to Examine:** All files.

- [ ] **Fallback Logic:**
    - **Action:** If no GPU is available, fall back to CPU (NumPy/Numba/Cython).
    - **Implementation:**
        - Allow user to select preferred device.
    - **Files to Examine:** All files.

- [ ] **Data Transfer:**
    - **Action:** Minimise host-device transfers. Keep data on GPU as much as possible.
    - **Implementation:**
        - Use pinned memory for fast transfers.
    - **Files to Examine:** All files.

- [ ] **Error Handling:**
    - **Action:** Gracefully handle GPU errors and out-of-memory conditions.
    - **Implementation:**
        - Log and notify the user.
    - **Files to Examine:** All files.

### Resource Assessment Widget

- [ ] **Widget Design:**
    - **Action:** Create a widget that scans available system resources (CPU cores, RAM, GPUs).
    - **Implementation:**
        - Display detected devices and their properties (e.g., GPU model, VRAM, CUDA/ROCm version).
    - **Files to Examine:** `gui/resource_assessment_widget.py` (new file).

- [ ] **Best Use Suggestion:**
    - **Action:** Based on dataset size and available resources, suggest the optimal processing mode.
    - **Implementation:**
        - (CPU single-threaded, CPU multi-threaded, GPU batch, distributed/Dask).
        - Provide recommendations and allow user override.
    - **Files to Examine:** `gui/resource_assessment_widget.py` (new file).

- [ ] **Integration:**
    - **Action:** On widget startup, run resource detection routines.
    - **Implementation:**
        - Use `psutil` for CPU/RAM, `cupy`/`torch` for GPU.
        - Display results in a user-friendly format.
    - **Files to Examine:** `gui/resource_assessment_widget.py` (new file).

- [ ] **Advanced Options:**
    - **Action:** Allow users to select device, set chunk/batch size, and enable/disable GPU acceleration.
    - **Implementation:**
        - Warn if resources are insufficient for the requested operation.
    - **Files to Examine:** `gui/resource_assessment_widget.py` (new file).

- [ ] **Extensibility:**
    - **Action:** Design widget to support future hardware (e.g., multi-GPU, cloud resources).
    - **Implementation:**
        - Ensure the widget is modular and can be easily extended.
    - **Files to Examine:** `gui/resource_assessment_widget.py` (new file).