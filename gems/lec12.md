### 1. The Fundamental Need for Schedulers  
**Key Points**  
- Scheduling is essential when multiple resource consumers compete for a scare set of shared resources.  
- No need to schedule if only one process or as many CPUs as processes (e.g., 2 processes with 2 CPU cores).  
- Scheduler complexity and overhead justify using scheduling only when necessary.  
- Schedulers enable multiplexing of scarce resources, ensuring fairness and good resource utilization.  
- Analogy to economic systems: scheduling is akin to distributing limited resources fairly among multiple consumers.  

_No explicit example problem here, but the professor emphasizes the fundamental principles behind why scheduling is needed. Important for deeply understanding the "when and why" of scheduling, which is a fundamental exam concept. The economic analogy is useful to conceptualize scheduling in a broader context._  

---  

### 2. Example: Why Elevator Scheduling is Like Disk Scheduling  
**Key Points**  
- Disks with rotating platters have significant overhead in switching between I/O requests leading to specialized disk scheduling algorithms.  
- Elevator scheduling analogy: naive first come first serve leads to excessive movement similar to poor disk scheduling.  
- Elevator scheduler optimizes by going through floors in one direction and picking up requests on the way, batching requests to minimize switching overhead.  
- Actuation delay and switching costs are crucial system assumptions affecting scheduling policies.  
- Declarative elevator systems (like coda elevators) use input specifying exact destination floors, enabling optimized batching compared to simple up/down calls.  

**Problem statement:**  
- Would you like an elevator using first come first serve (FCFS) scheduling? Why or why not?  
- How is an elevator schedule similar/different from disk I/O scheduling?  

**Solution:**  
- FCFS elevator is undesirable because it leads to inefficient and excessive travel times.  
- Like disk I/O, switching between requests incurs significant overhead, so it's better to batch requests heading in the same direction — similar to an elevator picking up all passengers going up before reversing direction.  
- Disk elevator scheduler tries to reorder requests to minimize disk platter movement.  
- The coda elevator introduces declarative requests with precise floor destinations, enabling smarter scheduling decisions beyond simple FCFS or elevator-style scheduling.  

_This is a concrete example given in lecture with a direct analogy between elevator scheduling and disk I/O scheduling. The professor explicitly points out the analogy and its impact on scheduling design — very likely to be an exam discussion or conceptual question._  

---  

### 3. Scheduling Goals / Metrics and Their Examples  
**Key Points**  
- Scheduler goals vary widely depending on context: throughput maximization, response time minimization, latency SLO attainment, cost minimization.  
- These different goals imply different optimal policies or tradeoffs.  
- Example throughput scheduling in disks: orders of magnitude performance difference depending on scheduling policy.  
- Latency SLOs correspond to deadlines or latency budgets needing constraint satisfaction rather than simple minimization.  
- Examples: LLM inter-token latency as a latency SLO problem. ad-serving latency for user engagement and revenue impact.  

_No direct problem stated, but highly important conceptual content laying the foundation for understanding scheduler design goals and their impact on policy choices. The professor explicitly mentions this as fundamental exam material ("how do you know that the scheduler is doing a good job?")_  

---  

### 4. Explanation of Latency Metrics: PDF, CDF, Tail Latency & Their Importance  
**Key Points**  
- Review of probability distribution function (PDF) and cumulative distribution function (CDF).  
- CDF is used to measure end-to-end response times in schedulers (Lab 3 will involve this measurement).  
- Tail latency corresponds to the very high percentile latencies (e.g., 99th percentile latency).  
- Tail latency matters for online platforms, where even 1% slow requests can cause user drop-off and financial loss.  
- Example graph of latency CDF showing 99th percentile latency and its relation to latency SLO deadline.  
- The distribution of response times arises from both service time and waiting time.  

_No specific question/problem solved, but the professor says: "if I were to ask you about questions about the CDF, you should know it inside out." This is a clear exam hint about the significance of understanding CDF, tail latency, and latency SLO concepts._  

---  

### 5. Schedulers for Long Running vs Short Running Jobs and Preemption  
**Key Points**  
- Round Robin is good for long running jobs because it preempts tasks to avoid head of line blocking and long wait times.  
- First come first serve is bad for long running jobs due to starvation and blocking.  
- Shortest Job First (SJF) does not require preemption, you run shortest job to completion.  
- Shortest Remaining Time (SRT) requires preemption to switch when shorter jobs arrive.  
- Preemptive vs non-preemptive scheduling choice depends on overhead and workload mix.  

**Problem statement:**  
- For long running jobs, which scheduler makes sense and why?  
- For short running jobs, which scheduler is better and is preemption required?  

**Solution:**  
- Long running jobs do better with Round Robin because preemption avoids blocking and long waits (head-of-line blocking problem).  
- Short running jobs do better with shortest job first variants, where SJF can be non-preemptive but SRT requires preemption.  
- Preemption adds overhead, so must balance cost-benefit.  

_This is a fundamental conceptual example connecting scheduling policies to workload characteristics. Important exam material, especially for justification of scheduler choice._  

---  

### 6. Delayed Scheduling Example (from Research and Google Borg Conversations)  
**Key Points**  
- Instead of scheduling a task immediately, delay scheduling to increase probability of preferred resource allocation.  
- Example: a task waits 5 seconds before placing, allowing better matching to preferred nodes.  
- This introduces a tradeoff: non work-preserving decisions — delay now to get better outcomes later.  
- Counterintuitive but effective, was debated with Google engineers.  
- This relates to lazy allocation policies.  

_An important research example illustrating tradeoffs in scheduling decisions, with practical implications. The professor highlights this discussion as a notable insight from their dissertation work and research._  

---  

### 7. Power of Two Choices Scheduling Policy  
**Key Points**  
- Simple algorithm: choose two nodes at random, assign task to the less loaded.  
- Complexity O(1) w.r.t number of resources, very efficient.  
- Provable guarantees on load balancing.  
- Implicit assumption: tasks are short and fine-grained ("fluidity" concept).  
- When tasks are large ("dropping bricks"), policy may not work well (risk of overloading some nodes).   

_An example of a simple but powerful scheduling policy introduced in lecture, with discussion of assumptions and limitations. Important conceptual material for the exam._  

---  

### 8. Costs of Scheduling: Context Switch Overhead, Cache and TLB Effects  
**Key Points**  
- Context switching overhead includes CPU time, plus significant cache and TLB flush costs.  
- High frequency context switches (e.g., every 10ms with 10ms overhead) drastically reduce utilization (potentially 50%).  
- Cache/TLB flush cause CPU stalls and increase runtime of processes after switches.  
- Scheduling complexity matters: some policies are O(N), others O(1), impacting scalability with number of tasks.  
- Example: power of two choices has O(1) complexity, while combinatorial scheduling (Tetris Cat) is expensive.  
- Scheduling time complexity must be small fraction of task runtime to be worthwhile.  

_Though no direct solved problem, the professor stresses the importance of understanding these costs and their tradeoffs, something likely to appear in exam questions about overhead and complexity._  

---  

### 9. Comparison of Scheduling Policies for Different Performance Metrics (Preview of Round Robin Discussion)  
**Key Points**  
- Different policies optimize for different objectives (throughput, latency, fairness, etc.)  
- No universal best scheduling solution; conflicting goals exist.  
- Scheduling is a complex design problem balancing tradeoffs like simplicity, cost, performance.  
- In next lecture, Round Robin policy will be analyzed in detail with respect to how poorly it can perform depending on success metrics chosen.  
- This preview hints at exam questions about analyzing scheduling policies and their tradeoffs.  

_The professor explicitly says, "If I were to ask you this on the exam" about understanding scheduler goals, metrics, and tradeoffs, especially for Round Robin, so this is an important anticipation for students._  

---  

# Summary of Examples and Exam-Relevant Points Extracted:  

| # | Topic/Example                                   | Exam Relevance & Notes                                |  
|---|------------------------------------------------|-------------------------------------------------------|  
| 1 | When do we need schedulers? (multi-consumer, scarce resource) | Fundamental principle of scheduling use cases.      |  
| 2 | Elevator scheduling analogy for disk scheduling | Concrete example demonstrating scheduling decisions and overhead assumptions. |  
| 3 | Scheduling goals (throughput, latency, latency SLO, cost) | Conceptual understanding of how to evaluate schedulers. |  
| 4 | CDF/PDF and tail latency explanation | Key for latency measurement and understanding tail latency importance (Lab 3). |  
| 5 | Long running vs short running jobs and preemption choices | Important for choosing scheduling policies based on workload characteristics. |  
| 6 | Delayed scheduling non work-preserving example | Research insight into scheduler design tradeoffs and tactics, useful concept. |  
| 7 | Power of two choices scheduling policy and assumptions | Efficient scheduling example with limitations, useful for exam theory. |  
| 8 | Costs of context switching including cache/TLB impacts | Important performance overhead considerations for scheduling design. |  
| 9 | Preview of Round Robin policy and tradeoffs | Expect detailed analysis and questions on Round Robin’s performance tradeoffs. |  

Each of these points either contains an example the professor discussed in detail, an exam hint ("if I were to ask you this on the exam"), or an emphasized fundamental aspect of scheduling. Students should be able to explain, solve, or discuss these topics and examples confidently for exam preparation.