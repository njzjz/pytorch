#include "vulkan_perf_utils.h"

#if defined(USE_VULKAN_GPU_DIAGNOSTICS) && defined(__ANDROID__)
extern const float NANOSECONDS_IN_SECOND = 1000000000.0;

// This function aggregate the latency of all invoked shaders except
// `vulkan.nchw_to_image` and `vulkan.image_to_nchw`, which are moving data
// between CPU and GPU memory.
extern void extractTotalShaderResultsAndSetState(benchmark::State& state) {
  at::native::vulkan::api::context()->querypool().extract_results();

  uint64_t sum_shader_latency_in_nanoseconds = 0;
  auto result_aggregator =
      [&sum_shader_latency_in_nanoseconds](
          const at::native::vulkan::api::ShaderDuration& s) {
        if (s.kernel_name != "vulkan.nchw_to_image" &&
            s.kernel_name != "vulkan.image_to_nchw") {
          sum_shader_latency_in_nanoseconds += s.execution_duration_ns;
        }
      };
  at::native::vulkan::api::context()->querypool().shader_log_for_each(
      result_aggregator);

  float sum_shader_latency_in_seconds =
      sum_shader_latency_in_nanoseconds / NANOSECONDS_IN_SECOND;
  state.SetIterationTime(sum_shader_latency_in_seconds);
}

// This function aggregates the latency of a specific operator with name `op_name`.
extern void extractTotalOpResultsAndSetState(
    benchmark::State& state,
    const char* op_name) {
  at::native::vulkan::api::context()->querypool().extract_results();
  float total_op_time =
      at::native::vulkan::api::context()->querypool().get_total_op_ns(op_name) /
      NANOSECONDS_IN_SECOND;
  state.SetIterationTime(total_op_time);
}
#endif
