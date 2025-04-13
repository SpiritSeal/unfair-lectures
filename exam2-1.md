Below is an exam synthesizing multiple design‐oriented questions that build on the topics covered across the lectures. In this exam you are asked not only to “do the math” but also to justify design decisions from first principles. You may be asked to diagram systems, list trade–offs, and explain ordering or permission–control mechanisms. (Do not simply list answers; provide detailed explanations and justifications.) You have roughly 3–5 hours for the exam.

──────────────────────────────
Problem 1: Virtual Memory and Copy‑on‑Write Design [Estimated Effort: 45min]

Imagine you are designing a minimalist operating system for a 32‑bit architecture that implements process forking via copy‐on‑write (CoW). In your design, all user processes share their initial physical frames immediately after a fork, with the expectation that a page “split” (and duplication) occurs only when a process writes to a shared page.

1A. Explain how you would use the logical permission bits (which signal that a process is allowed to access an address) and the physical permission bits (which control the CPU’s actual write access) to support CoW. In your answer, describe the initial state of page table entries immediately after fork and what happens when a process attempts to write to a shared page.

1B. Describe how you would determine—using a reference count or a mapping graph—whether a physical frame is shared between processes. What criteria do you use to decide to trigger a copy? Explain the consequences for higher-level data structures (e.g., page tables or even page directories) if they become shared.

1C. Consider that your lab constraints limit you so that only the last‐level physical frames need to support CoW (that is, you need not copy the page directory or intermediate page table pages). Discuss the advantages and any potential pitfalls of this design choice compared to an approach where you implement CoW at every level of the mapping hierarchy.

──────────────────────────────
Problem 2: Crash Consistency and Journaling in a File System [Estimated Effort: 45min]

You are asked to design a journaling layer for a file system that must guarantee crash consistency. The file system must enforce that when metadata (such as the inode or directory entries) becomes visible externally, all corresponding data blocks have already been safely written.

2A. Describe a journal design that uses ordering primitives (such as flush operations) to enforce the “happens‐before” relationship between writing a data block and writing its associated commit record (C_i) in the journal. Include in your answer a diagram (or a clear description) of the ordering between data block writes, log entries (E_i), and commits.

2B. Some file system updates are implemented via shadowing. Explain how you would design a shadowing mechanism that uses a Boolean “shadow bit” and two physical copies of a data block to achieve atomic updates. What is the ordering of operations needed and how does the atomic flipping of the shadow bit ensure that the system never sees a “partial” update?

2C. Consider a scenario in which you have two file descriptors associated with two files. A process writes to both files and then a crash occurs. Discuss the challenges in cross–descriptor ordering. What design decisions in your journaling protocol can maximize consistency (or “valid prefix” properties) when writes to different files are interleaved in the same journal? Explain any performance implications.

──────────────────────────────
Problem 3: Scheduler Design for a Microkernel Environment [Estimated Effort: 40min]

In a microkernel system, many fundamental services (such as file system and network stack) run in user space while a compute‑intensive application is also running. You are charged with designing a scheduler that must handle both I/O‐bound user services and CPU–intensive processes, with a very high number of processes relative to available CPUs.

3A. Identify and define two quantifiable success metrics that would be most relevant for such a heterogeneous workload. Explain why each metric is important.

3B. Propose a scheduling policy that could accommodate both interactive (or low‐CPU I/O–bound) services and long, compute–intensive jobs. In your answer, discuss the trade-offs (for example, fairness versus latency) and how your design might use preemption (or even admission control) to ensure that high-priority latency-sensitive tasks are not starved by background compute jobs.

3C. Suppose a user-space service in your microkernel (for instance, a networking daemon) has an internal dependency—it calls into another service (e.g., memory service) that previously ran in isolation. Explain how this dependency affects the scheduler’s design, particularly regarding failure isolation and priority ordering among processes.

──────────────────────────────
Problem 4: Paging Design and TLB Trade–Offs [Estimated Effort: 35min]

You are tasked with designing a paging mechanism for a new operating system running on a 32‑bit processor. Two candidate designs are under consideration:
  (i) a two‑level paging system with 10 bits for the page directory, 10 bits for the page table, and 12 bits for the offset, and
  (ii) a single‑level paging system that uses a “huge” page design where pages are 4 MB in size.

4A. For the two‑level paging system, explain the memory overhead associated with holding page tables for a process with sparse memory usage. How does the allocation of a full page for a partially used page table impact the overall overhead?

4B. Discuss how the TLB (Translation Lookaside Buffer) hit ratio is influenced by page size. Compare the expected TLB coverage for the two–level system (with 4 KB pages) versus the huge page system (with 4 MB pages). What are the trade-offs—in terms of fragmentation and memory waste—when choosing between these designs?

4C. Given that the hardware provides a fixed number of TLB entries, justify which design might be more efficient for a server workload with a very large address space but many short-lived processes.

──────────────────────────────
Problem 5: Security and Policy Attack Vectors [Estimated Effort: 35min]

Recent lectures have emphasized that security must be designed with the assumption that an attacker may know all of the internal structure of your system (“Kerckhoffs’s Principle”). Consider a system where grades are managed in a university’s online portal. The system is supposed to be secure against unauthorized grade changes.

5A. Describe several potential attack vectors that an adversary might use to change grades despite the policy that “only a trusted administrator (or TA) may perform grade updates.” In your answer, discuss how design choices (such as reliance on obscurity or weak authentication) can lead to privilege escalation.

5B. Assume a real-world scenario in which a dependency error in policy management allows a student to be added into a privileged group (e.g., being mistakenly added to an administrator’s list). Explain how such a design flaw can lead to catastrophic breaches of isolation and why strict separation of authority (and careful policy administration) is crucial.

5C. Propose a design for a secure grade‐management system that mitigates these risks. Your answer should consider robust authentication, strict role isolation, and auditability. Describe how you would incorporate logging and ghost (or shadow) techniques so that even if some components are compromised, the integrity of grade data can eventually be restored.

──────────────────────────────
General Instructions:
 • For each problem, be prepared to justify your design choices quantitatively (e.g., overhead ratios, flush counts, TLB performance) as well as qualitatively (e.g., trade-offs between isolation and performance, failure propagation, and security implications).
 • Diagrams are encouraged where appropriate (for instance, in illustrating the mapping graph for copy-on-write or a timeline of flush ordering in journaling).
 • Answer every subpart in detail—explain all assumptions from first principles and discuss any potential edge cases.

Good luck with your exam!