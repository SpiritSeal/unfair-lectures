Below is an exam that explores many “big‐idea” design problems drawn from our lectures. Each problem presents a realistic scenario and then asks you to design or analyze a solution. You must explain your reasoning from first principles, describe trade-offs, and discuss how your design reflects limitations (or benefits) of the underlying mechanisms. (Do not simply recall class notes—ensure that you explain the “why” behind each design decision.) 

──────────────────────────────────────────────────────────────
Problem 1: Virtual Memory & Copy‐on‐Write Design [Estimated Effort: 45min]

A new operating system is being developed for a 32–bit architecture that supports processes with a 4‑GB virtual address space. To speed up process creation (fork), the design uses copy‑on‑write (CoW) so that physical frames are not duplicated at fork time but are shared until a write occurs. However, your system also supports shared libraries (where multiple processes map the same code in a read‐only manner) and demand paging with lazy allocation.

Part A. Describe your design for the copy‑on‑write mechanism. In your answer, cover the following points:
  • How you will “share” the parent's virtual mappings in the child without copying the underlying physical frames immediately.
  • The role and difference between logical permission bits and physical permission bits in enforcing CoW.
  • How your design uses a reference–count (or “graph-of-mappings” view) to decide when a physical frame is shared and thus triggers a CoW on a write attempt.
  • How you will trigger a trap upon a write and what steps are performed (allocation of a new frame, updating the page table and TLB, etc.)

Part B. Analyze the trade-offs of using lazy CoW versus an eager duplication strategy. In particular, compare:
  • The time complexity of fork under both approaches.
  • The overheads introduced by TLB invalidation and context switching when CoW copies are eventually performed.
  • Scenarios (such as heavy writes on the stack vs. read–only shared libraries) where one method outperforms the other.

Part C. Suppose that a process uses a “break” system call to request a large contiguous region of virtual memory that is initially zero‐filled. Explain how demand (lazy) allocation can be integrated with your CoW design to reduce upfront physical memory usage. What are the benefits and risks of this approach?

──────────────────────────────────────────────────────────────
Problem 2: Journaling and Crash Consistency in Filesystems [Estimated Effort: 40min]

Your filesystem is required to guarantee crash consistency while keeping write overhead as low as possible. To this end, you are considering a design that combines ordered logging with a shadowing mechanism. In your design, updates are first written to a log (with a separate commit region) so that in the event of a crash you can “replay” them. To reduce latency, the same physical block might be updated in two copies (an “active” version and a shadow copy), with a single “shadow bit” that indicates which copy is current.

Part A. Propose three unique designs for ordering writes that guarantee atomic persistence:
  (i) A design in which data writes are flushed before updating metadata in the journal.
  (ii) A design that uses a shadow bit to trigger a trap (or flush) only when the access bit is zero.
  (iii) A single‑level log merging design in which a flush is deferred until a group of writes is ready.
For each design, explain:
  • How the flush ordering ensures that once a commit record is visible the file system is in a valid state.
  • The potential performance overhead (e.g. number of required flushes or trap costs).

Part B. Describe a “valid prefix” invariant for your log. Explain how your design decides whether to read data from the log or from the data area upon recovery, taking into account the possibility of partial or corrupted log entries.

Part C. In your chosen design, discuss the effect on performance when a file’s writes interleave with many “meta‐updates” (for example, when directory entries and inodes are updated during file creation). How does global ordering (a single log for multiple files) affect the commit delay and what trade-offs does it introduce?

──────────────────────────────────────────────────────────────
Problem 3: Microkernel Scheduling and Service Isolation [Estimated Effort: 35min]

Imagine you are designing a microkernel-based OS called “uBuzz.” In your architecture, certain services (such as memory allocation, file services, and even networking) have been moved to user space. A computationally intensive ML training application (App A) runs alongside persistent services like the memory service (MS) and file service (FS), which are not CPU–intensive. In addition, a networking service (NS) has been factored out and later even becomes dependent on MS and FS.

Part A. Design a scheduling policy for uBuzz that must handle both heavy CPU–intensive processes (like your ML application) and continuously running low–CPU background services. In your answer, please:
  • Identify two quantitative success metrics (for example, throughput and tail latency) for system performance in this scenario.
  • Justify whether you would choose a preemptive or non–preemptive scheduler with respect to these metrics.
  • Discuss why simple FIFO or Round Robin scheduling might or might not be acceptable.

Part B. After an intern reassigns the networking (NS) service so that it indirectly depends on MS and FS, the ML application (A) now depends only on NS. However, the system still drops packets if NS cannot process within a strict 10‑ms deadline. Explain how you would change your scheduling policy to ensure that NS meets its time constraint, and analyze the trade-offs of your solution.

Part C. Reflect on the benefits of isolating OS services in a microkernel versus the overhead of additional context switches and increased dependency complexity. Has the microkernel design improved failure isolation for the ML application? Provide concrete arguments referring to service dependency graphs and failure closures.

──────────────────────────────────────────────────────────────
Problem 4: Security and Resource Sharing in System Design [Estimated Effort: 30min]

As security concerns are paramount, you have been asked to design a secure operating system component that resists both internal and supply–chain attacks.

Part A. Consider a scenario where a teacher’s account manages student grades on a central system (similar to the TA/Canvas Grade Attack scenario). Design a set of mechanisms (technical and policy–based) that prevent unauthorized grade changes, even if some low–privilege accounts or endpoints (e.g. a TA’s machine) are compromised.
  • Explain how isolation, privilege separation, and audit mechanisms can mitigate potential attack vectors.
  • Discuss how your design follows the principle that “the system must be secure even if the adversary knows everything about it” (Kerckhoffs’s Principle).

Part B. In another scenario, a popular open-source package (like the left–pad library) is suddenly removed from the central repository, breaking many applications. Propose a strategy for designing your build and dependency management system to be resilient against supply–chain attacks and sudden dependency failures.
  • Your answer should address dependency replication, strict versioning, and automatic integrity verification (for instance, via cryptographic signing and salted hashes).
  • Include a discussion on how these measures balance the trade-off between openness and secure control.

Part C. Finally, analyze the impact of traditional memory safety vulnerabilities such as buffer overflows in a legacy C code module versus the advantages offered by a memory–safe language (e.g., Rust) in system components. Provide design suggestions for transitioning legacy code to improve security without requiring a complete rewrite.

──────────────────────────────────────────────────────────────
Instructions:
• Answer each part using a clear explanation, diagrams (if helpful), and trade–off analysis.
• You may reference specific examples discussed in class to support your arguments.
• Ensure that your solutions address both the “what” and the “why” behind each design choice.

Good luck and happy designing!