"""
Benchmark suite for vLLM + ARM Axion Integration

Tests:
- TTFT (Time to First Token) with incremental routing
- Throughput with multiple concurrent requests
- Memory efficiency with quantization
- Routing accuracy and speed
"""

import sys
from pathlib import Path
import time
import asyncio
import numpy as np
from typing import List, Dict, Any
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from vllm_integration.vllm_axion_backend import AxionMultiExpertVLLM
from vllm_integration.livemind_orchestrator import LiveMindOrchestrator, GenerationRequest
from vllm_integration.semantic_router import IncrementalSemanticRouter


class VLLMAxionBenchmark:
    """Comprehensive benchmark suite"""

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize benchmark

        Args:
            config_path: Path to config file
        """
        print("🔧 Initializing benchmark suite...")

        # Load config
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Initialize system
        print(f"📦 Loading {len(self.config['experts'])} experts...")
        self.expert_system = AxionMultiExpertVLLM(self.config['experts'])

        print("🧠 Initializing orchestrator...")
        self.orchestrator = LiveMindOrchestrator(
            expert_system=self.expert_system,
            enable_consensus=self.config.get('enable_consensus', False),
            chunk_size=self.config.get('chunk_size', 64),
            routing_threshold=self.config.get('routing_threshold', 0.7)
        )

        print("✅ Benchmark suite ready!\n")

        # Results storage
        self.results = {
            'ttft': [],
            'latency': [],
            'throughput': [],
            'routing_accuracy': []
        }

    async def benchmark_ttft(
        self,
        prompts: List[str],
        num_runs: int = 5
    ) -> Dict[str, float]:
        """
        Benchmark Time to First Token with incremental routing

        Args:
            prompts: Test prompts of varying lengths
            num_runs: Number of runs per prompt

        Returns:
            TTFT statistics
        """
        print("📊 Benchmarking TTFT (Time to First Token)")
        print("=" * 60)

        ttft_samples = []

        for i, prompt in enumerate(prompts):
            print(f"\nPrompt {i+1}/{len(prompts)} (length: {len(prompt.split())} words)")

            for run in range(num_runs):
                request = GenerationRequest(
                    request_id=f"ttft_test_{i}_{run}",
                    prompt=prompt,
                    max_tokens=50,  # Short generation for TTFT measurement
                    stream=True
                )

                start_time = time.time()

                # Generate (will measure internal TTFT)
                result = await self.orchestrator.generate(request)

                ttft = result.time_to_first_token
                ttft_samples.append(ttft)

                print(f"  Run {run+1}: TTFT = {ttft*1000:.1f}ms, "
                      f"Chunks = {result.chunks_processed}")

        # Statistics
        stats = {
            'mean': np.mean(ttft_samples),
            'median': np.median(ttft_samples),
            'std': np.std(ttft_samples),
            'min': np.min(ttft_samples),
            'max': np.max(ttft_samples),
            'p95': np.percentile(ttft_samples, 95),
            'p99': np.percentile(ttft_samples, 99)
        }

        print(f"\n📈 TTFT Statistics:")
        print(f"  Mean:   {stats['mean']*1000:.1f}ms")
        print(f"  Median: {stats['median']*1000:.1f}ms")
        print(f"  P95:    {stats['p95']*1000:.1f}ms")
        print(f"  P99:    {stats['p99']*1000:.1f}ms")

        self.results['ttft'] = stats
        return stats

    async def benchmark_throughput(
        self,
        num_requests: int = 50,
        concurrent_requests: int = 10
    ) -> Dict[str, float]:
        """
        Benchmark throughput with concurrent requests

        Args:
            num_requests: Total number of requests
            concurrent_requests: Max concurrent requests

        Returns:
            Throughput statistics
        """
        print(f"\n📊 Benchmarking Throughput")
        print("=" * 60)
        print(f"Total requests: {num_requests}")
        print(f"Concurrent: {concurrent_requests}\n")

        # Test prompts
        test_prompts = [
            "Explain quantum computing in simple terms.",
            "Write a Python function for binary search.",
            "What are the benefits of PagedAttention?",
            "Describe the ARM Axion processor architecture.",
            "How does continuous batching improve throughput?"
        ] * (num_requests // 5 + 1)

        test_prompts = test_prompts[:num_requests]

        # Semaphore for concurrency control
        semaphore = asyncio.Semaphore(concurrent_requests)

        async def run_single_request(idx, prompt):
            async with semaphore:
                request = GenerationRequest(
                    request_id=f"throughput_test_{idx}",
                    prompt=prompt,
                    max_tokens=100,
                    stream=False
                )

                start = time.time()
                result = await self.orchestrator.generate(request)
                latency = time.time() - start

                return {
                    'latency': latency,
                    'tokens': result.tokens_generated
                }

        # Run all requests
        start_time = time.time()

        tasks = [
            run_single_request(i, prompt)
            for i, prompt in enumerate(test_prompts)
        ]

        results = await asyncio.gather(*tasks)

        total_time = time.time() - start_time

        # Calculate stats
        latencies = [r['latency'] for r in results]
        total_tokens = sum(r['tokens'] for r in results)

        throughput_rps = num_requests / total_time
        throughput_tps = total_tokens / total_time

        stats = {
            'requests_per_second': throughput_rps,
            'tokens_per_second': throughput_tps,
            'total_time': total_time,
            'mean_latency': np.mean(latencies),
            'p95_latency': np.percentile(latencies, 95),
            'p99_latency': np.percentile(latencies, 99)
        }

        print(f"📈 Throughput Results:")
        print(f"  Requests/sec: {stats['requests_per_second']:.2f}")
        print(f"  Tokens/sec:   {stats['tokens_per_second']:.2f}")
        print(f"  Total time:   {stats['total_time']:.2f}s")
        print(f"  Mean latency: {stats['mean_latency']*1000:.1f}ms")
        print(f"  P95 latency:  {stats['p95_latency']*1000:.1f}ms")

        self.results['throughput'] = stats
        return stats

    def benchmark_routing_accuracy(
        self,
        test_cases: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Benchmark routing accuracy

        Args:
            test_cases: List of {'text': str, 'expected_domain': str}

        Returns:
            Accuracy statistics
        """
        print(f"\n📊 Benchmarking Routing Accuracy")
        print("=" * 60)

        correct = 0
        total = len(test_cases)

        results_detail = []

        for i, test_case in enumerate(test_cases):
            text = test_case['text']
            expected = test_case['expected_domain']

            # Get routing prediction
            request_id = f"routing_test_{i}"
            self.orchestrator.router.start_request(request_id)

            prediction = self.orchestrator.router.process_chunk(
                request_id,
                text
            )

            # Get predicted domain
            predicted_expert = prediction.expert_ids[0]
            predicted_domain = self.orchestrator.router.expert_domains.get(
                predicted_expert,
                'unknown'
            )

            is_correct = predicted_domain == expected

            if is_correct:
                correct += 1

            results_detail.append({
                'text': text[:50] + '...',
                'expected': expected,
                'predicted': predicted_domain,
                'confidence': prediction.confidence,
                'correct': is_correct
            })

            status = "✅" if is_correct else "❌"
            print(f"  {status} Test {i+1}: '{text[:40]}...'")
            print(f"      Expected: {expected}, Got: {predicted_domain} "
                  f"(conf: {prediction.confidence:.2f})")

        accuracy = correct / total

        stats = {
            'accuracy': accuracy,
            'correct': correct,
            'total': total,
            'details': results_detail
        }

        print(f"\n📈 Routing Accuracy: {accuracy*100:.1f}% ({correct}/{total})")

        self.results['routing_accuracy'] = stats
        return stats

    def benchmark_memory_efficiency(self) -> Dict[str, Any]:
        """
        Benchmark memory efficiency with quantization

        Returns:
            Memory statistics
        """
        print(f"\n📊 Memory Efficiency Analysis")
        print("=" * 60)

        expert_info = []

        for expert_id, info in self.expert_system.experts.items():
            config = info['config']
            engine = info['engine']

            # Estimate memory usage
            # This is approximate - real measurement would need actual vLLM metrics
            quantization = config.quantization
            model_path = config.model_path

            # Rough estimate based on model name
            if '7b' in model_path.lower() or '7B' in model_path:
                params = 7_000_000_000
            elif '13b' in model_path.lower() or '13B' in model_path:
                params = 13_000_000_000
            elif '70b' in model_path.lower() or '70B' in model_path:
                params = 70_000_000_000
            else:
                params = 7_000_000_000  # Default assumption

            # Memory calculation
            if quantization == 'q4_0':
                bytes_per_param = 0.5
            elif quantization == 'q8_0':
                bytes_per_param = 1.0
            elif quantization in ['awq', 'gptq']:
                bytes_per_param = 0.5  # ~4-bit
            else:
                bytes_per_param = 2.0  # FP16

            memory_gb = (params * bytes_per_param) / 1e9

            expert_info.append({
                'expert_id': expert_id,
                'domain': info['domain'],
                'model': model_path,
                'quantization': quantization or 'fp16',
                'params': params,
                'memory_gb': memory_gb
            })

            print(f"\n  Expert: {expert_id}")
            print(f"    Domain: {info['domain']}")
            print(f"    Model: {model_path}")
            print(f"    Quantization: {quantization or 'fp16'}")
            print(f"    Parameters: {params/1e9:.1f}B")
            print(f"    Est. Memory: {memory_gb:.1f} GB")

        total_memory = sum(e['memory_gb'] for e in expert_info)

        print(f"\n📦 Total Memory Usage: {total_memory:.1f} GB")

        stats = {
            'experts': expert_info,
            'total_memory_gb': total_memory,
            'num_experts': len(expert_info)
        }

        return stats

    def save_results(self, output_path: str = "benchmark_results.json"):
        """Save benchmark results to file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {output_path}")

    async def run_full_suite(self):
        """Run complete benchmark suite"""
        print("\n" + "=" * 60)
        print("🏆 vLLM + ARM Axion Full Benchmark Suite")
        print("=" * 60)

        # 1. TTFT Benchmark
        test_prompts = [
            "What is ARM Axion?",
            "Explain PagedAttention in vLLM. How does it improve memory efficiency and enable higher batch sizes?",
            "Write a detailed implementation of a binary search tree in Python with insert, delete, and search operations. Include proper error handling and documentation." * 5
        ]

        await self.benchmark_ttft(test_prompts, num_runs=3)

        # 2. Throughput Benchmark
        await self.benchmark_throughput(num_requests=30, concurrent_requests=10)

        # 3. Routing Accuracy
        test_cases = [
            {'text': 'What are the legal implications of this contract clause?', 'expected_domain': 'legal'},
            {'text': 'Implement a quicksort algorithm in Python', 'expected_domain': 'technical'},
            {'text': 'What is the best investment strategy for retirement?', 'expected_domain': 'finance'},
            {'text': 'Patient shows symptoms of high fever and headache', 'expected_domain': 'medical'},
            {'text': 'Tell me about the weather today', 'expected_domain': 'general'},
        ]

        # Map to actual expert domains
        actual_domains = set(
            info['domain']
            for info in self.expert_system.experts.values()
        )

        filtered_test_cases = [
            tc for tc in test_cases
            if tc['expected_domain'] in actual_domains or tc['expected_domain'] == 'general'
        ]

        if filtered_test_cases:
            self.benchmark_routing_accuracy(filtered_test_cases)

        # 4. Memory Efficiency
        self.benchmark_memory_efficiency()

        # Save results
        self.save_results()

        print("\n" + "=" * 60)
        print("✅ Benchmark suite completed!")
        print("=" * 60)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="vLLM + ARM Axion Benchmark")
    parser.add_argument("--config", type=str, default="config.json", help="Config file path")
    parser.add_argument("--output", type=str, default="benchmark_results.json", help="Output file")

    args = parser.parse_args()

    try:
        benchmark = VLLMAxionBenchmark(config_path=args.config)

        asyncio.run(benchmark.run_full_suite())

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        import traceback
        traceback.print_exc()
