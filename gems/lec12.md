Below is a detailed list of examples, questions, and “problems”—along with the professor’s line‐of‐thinking and answers—that were interwoven with the main lecture content and which may very well be “exam material” (or at least serve as excellent study questions). In what follows, I’ve “copied” the phrasing of the problem as it appeared (or was implicitly posed) during the lecture and the professor’s explanation/solution. Note that although the professor did not always say, “if I were to ask you this on the exam…”, many of these examples were treated as fundamental or were discussed in depth (or even questioned in class) so that an attentive listener would be well prepared for exam questions. Here are the key examples:

────────────────────────────
1. When Is a Scheduler Needed?  
────────────────────────────
 Problem (posed interactively):  
  “Could you get away and get along without schedulers? In other words, when do you need a scheduler? For example, if there is only one process or if there are two processes and two cores, do you really need a scheduler?”  

 Professor’s Explanation/Solution:  
  • The scheduler is only truly needed when you have multiple resource consumers competing for a scarce pool of resources.  
  • If you have only one process, no scheduler is needed.  
  • Even in a two–process/two–core setting, if you can statically bind a process to a core, you may obviate the need for a runtime scheduler.  
  • The general rule is that a scheduler becomes essential when (a) there are multiple processes/threads sharing a limited resource and (b) you need to enforce fairness, ensure isolation, or maximize resource utilization.

────────────────────────────
2. The Elevator (and Disk) Scheduling Analogy  
────────────────────────────
 Problem (imagine this exam question):  
  “Imagine an elevator that operates on a simple first-come, first-served principle. Would such a system work well in a busy building? Explain why a scheduler (or a smarter ‘elevator algorithm’) is needed for efficient service.”  

 Professor’s Explanation/Solution:  
  • A plain first-come–first-served elevator will visit floors in the order of request arrival and may waste time by moving back and forth inefficiently.  
  • Instead, an ‘elevator scheduler’ might wait a little and batch requests that are going in the same direction so that during one trip, many calls are satisfied.  
  • The same idea applies to disk scheduling (e.g., “elevator” or SCAN algorithms): due to high actuation delays (from rotating platters, for example), it is far more efficient to reorder disk I/O requests so that a whole batch is handled during one disk spin.
  • In turn, this reasoning illustrates that in any system where switching between tasks or requests incurs nontrivial overhead, the scheduling policy matters greatly for quality of service.

────────────────────────────
3. Cumulative Distribution Function (CDF) and Tail Latency  
────────────────────────────
 Problem (likely exam question):  
  “Define a cumulative distribution function (CDF) in the context of end-to-end response times. What is ‘tail latency’, and how would you explain the relationship between the two (for example, the 99th percentile)?”  

 Professor’s Explanation/Solution:  
  • The CDF is defined such that, for a given time x, it gives the probability that a response (or latency) is less than or equal to x.  
  • Tail latency refers to the behavior of the distribution near its extreme values—that is, the long “tail” or the worst-case (high percentile) response times.  
  • For instance, if the 99th percentile latency is 35.67 milliseconds and your latency Service-Level Objective (SLO) is 36 ms, then almost every request meets the SLO.  
  • It is important to understand how to construct and interpret these curves because they help in measuring not only average performance but also the worst-case delays that can impact user experience.

────────────────────────────
4. Scheduling Objectives: Throughput, Response Time, and Latency SLOs  
────────────────────────────
 Problem (conceptual exam question):  
  “Discuss the trade-offs in different scheduling objectives. How do throughput, average response time minimization, and meeting tail-latency (or deadline) SLOs differ in what they optimize?”  

 Professor’s Explanation/Solution:  
  • A good scheduler is intended to maximize the “amount of work done” or throughput.  
  • In some cases, the goal is to reduce waiting time or overall response time (e.g., for interactive tasks or networked requests).  
  • In others, the emphasis is on meeting strict latency Service-Level Objectives (such as ensuring the 99th percentile latency is below a threshold).  
  • The differences imply that optimizing one metric does not automatically optimize the other—hence the need to choose policies based on the target success metric (for example, using disk “elevator” scheduling to reduce rotational delays).

────────────────────────────
5. Shortest Job First (SJF) vs. Shortest Remaining Time First (SRTF)  
────────────────────────────
 Problem (exam-style):  
  “Describe the difference between non-preemptive Shortest Job First (SJF) scheduling and preemptive Shortest Remaining Time First (SRTF) scheduling. When might each be preferred?”  

 Professor’s Explanation/Solution:  
  • In Shortest Job First, once a job is picked, it runs to completion; there is no preemption, so the scheduler does not have to interrupt a running process.  
  • In the Shortest Remaining Time First policy, the scheduler continually reassesses the remaining execution time, and if a new job with a shorter remaining time arrives, it preempts the current job.  
  • This distinction is critical because the cost of preemption (e.g., context-switch overhead and TLB/cache invalidations) may outweigh the benefits if jobs are too short.  
  • The professor emphasized that SJF does not require preemption but SRTF does—an insight potentially worth being able to discuss on an exam.

────────────────────────────
6. Delayed (Lazy) Scheduling  
────────────────────────────
 Problem (exam question possibility):  
  “Explain the concept of delayed (or lazy) scheduling. Provide an example in which deferring the scheduling decision for a fixed amount of time (say, 5 seconds) can lead to a more preferred resource allocation.”  

 Professor’s Explanation/Solution:  
  • In delayed scheduling, instead of immediately assigning a task to a resource, the system waits for a short fixed period, allowing for the possibility of getting a ‘better’ resource allocation (for instance, a node with more available capacity or one that better meets job preferences).  
  • The professor illustrated that even though this decision is non–work–preserving (i.e., a delay is introduced intentionally), waiting can result in higher probability of preferred placement and therefore overall better performance.
  • This example builds on his discussions with teams (e.g., Google’s Borg team) where “waiting” is sometimes the superior design choice.

────────────────────────────
7. Power of Two Choices  
────────────────────────────
 Problem (potential exam question):  
  “Describe the power of two choices algorithm in the context of load balancing. What is its time complexity and what implicit assumptions does it make about task duration?”  

 Professor’s Explanation/Solution:  
  • The algorithm is used to pick between two randomly chosen resources and then assign the incoming task to the less loaded one.
  • Its key appeal is that its scheduling decision has O(1) complexity independent of the total number of resources.
  • However, an implicit assumption is that the jobs are short—if the tasks were long, the dynamics and benefits of making only two comparisons might change.
  • This policy is presented as a simple yet powerful alternative to more computationally intensive allocation algorithms.

────────────────────────────
8. Overheads and Costs in Scheduling  
────────────────────────────
 Problem (exam-style):  
  “Identify and discuss the nontrivial overheads imposed by scheduling. How do factors such as context switching, cache and TLB invalidation, and scheduler algorithm time complexity impact overall system performance?”  

 Professor’s Explanation/Solution:  
  • Every scheduling decision introduces overhead that is not free. For example:
   – Context switching requires saving and restoring state.
   – Frequent switching can lead to significant cache and TLB (Translation Lookaside Buffer) thrashing; each switch flushes out entries that must later be repopulated.
   – Moreover, the algorithmic complexity of the scheduling decision itself (e.g., whether it is O(1) like in the power of two choices, or O(N) in a more naive policy) matters, especially when tasks are very short.
  • The professor stressed that these costs must be weighed against any potential benefit: if the scheduler’s overhead is comparable to the task service time, you could end up undermining system utilization.

────────────────────────────
9. Global Versus Local (Centralized Versus Decentralized) Scheduling  
────────────────────────────
 Problem (for exam discussion):  
  “Compare centralized (global) and decentralized (local) scheduling approaches in distributed systems. What are the trade-offs in terms of resource state visibility and system scalability?”  

 Professor’s Explanation/Solution:  
  • In a global scheduler, a single entity has access to the complete resource state (all cores/GPUs/nodes), potentially allowing for more optimized placement decisions.  
  • However, a global scheduler may face scalability challenges as the number of resources increases.  
  • In contrast, local schedulers operate only with local state information; they are more scalable because they avoid a centralized bottleneck, yet might be less optimal as decisions are made without full visibility.
  • This trade-off is a recurring theme in systems design, and understanding it is fundamental to reasoning about scheduler design.

────────────────────────────
10. The “Two Out of Three” Trade-Off in Scheduling  
────────────────────────────
 Problem (conceptual exam question):  
  “Explain why in scheduling systems you cannot simultaneously achieve simplicity, low cost, and high performance. Discuss how the ‘two out of three’ trade-off manifests in scheduler design.”  

 Professor’s Explanation/Solution:  
  • The professor pointed out that many scheduling designs can optimize for any two of these attributes simultaneously but never all three.  
  • For example, a highly efficient (high-performance) scheduler might be extremely complex and expensive to maintain, while a simple-scheduler may not yield the best performance or may be cost-prohibitive in terms of resource usage.
  • Being able to articulate and analyze these trade-offs shows understanding of not just “how” but also “why” certain scheduling decisions are made.

────────────────────────────
11. Scheduler Design Under Latency SLO Constraints  
────────────────────────────
 Problem (modern exam example):  
  “How does a scheduler adapt when there is a hard latency SLO (Service-Level Objective)? Provide an example such as ad serving or large language model token generation and discuss what it means to ‘maximize latency SLO attainment’.”  

 Professor’s Explanation/Solution:  
  • Scheduler design must account for deadlines or latency budgets. In ad serving, for instance, if a decision is not made within a set number of milliseconds, the revenue impact via click-through rate can be severe.  
  • Similarly, modern applications (such as LLM inference) have explicit target latencies (e.g., time between tokens or TBT SLO).  
  • The goal is not to minimize response time arbitrarily but to ensure that the worst-case (tail) latencies remain within the acceptable bound defined by the SLO.

────────────────────────────
12. Assumptions Underlying Scheduling Policies  
────────────────────────────
 Problem (exam discussion point):  
  “Many scheduling policies are built on implicit assumptions. Identify typical assumptions (such as resource homogeneity and high liquidity of tasks) and explain how deviations from these assumptions affect performance and complexity.”  

 Professor’s Explanation/Solution:  
  • One common assumption is that resources are homogeneous (indistinguishable in terms of capacity), which simplifies allocation.  
  • Another is that tasks are ‘liquid’—meaning they are fine-grained and easily distributed.  
  • If resources become heterogeneous or tasks are large (think bricks versus sand), then many of the simple policies (such as power of two choices) are either less effective or require more sophisticated (and complex) approaches.
  • The faculty’s broader point is that when designing systems with scheduling, it is critical to “externalize” and scrutinize these assumptions, especially when you propose a fundamentally different approach from what is conventional.

────────────────────────────
Closing Note
────────────────────────────
Throughout this lecture, the professor also reminded students about exam logistics and practical hints (e.g., “bring your charged laptop” and the exam date on March 11). However, the core concepts above represent key examples and reasoning patterns that if you were asked an exam question – for example, “explain the overheads of scheduling” or “explain in detail the elevator (disk) scheduling analogy” – you would need to structure your answer along the lines discussed.

Studying these examples, ensuring that you can work through the reasoning and apply first principles (as the professor emphasizes), is essential for both understanding and exam preparation.