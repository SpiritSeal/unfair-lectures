Below is a list of the exam‐relevant examples and questions (with the professor’s hints and answers) that I extracted from the transcript. Notice that the professor interweaves these “if I were to ask you on the exam…”–style cues with his explanation of the design choices in virtual memory management, copy‐on‐write forking, and permission control. Read through these notes carefully so that you can (1) solve the example yourself and (2) know what concepts you might be quizzed on later.

──────────────────────────────
1. Copy‐on‐Write Fork: Do You Need to Copy the Entire Virtual Address Space on Fork?

• Exam–type question (the professor even hints “if I were to ask you this on the exam…”)  
 Problem: When performing a fork, must the entire virtual address space (including the page directory, page table pages, and all physical frames) be duplicated immediately?  
 Professor’s reasoning and answer:
  – Logically, isolation requires that the child process appears to have its own copy.
  – Physically, however, you can “lie” to the process and share the physical frames immediately after fork.
  – Then—if/when a process writes to a shared physical frame—the kernel traps the write and makes a copy of that frame (the “copy on write” operation).
  – Thus, the efficient (lazy) way is to share mappings at fork and only copy on mutation.
  Important: This underpins many decisions later when discussing which mappings (page directories, PT pages, physical frames) are copied “eagerly” versus lazily.
  Your exam answer should explain that in a fork, only on-demand (write) copying is required so that you do not immediately duplicate the process’s memory.

──────────────────────────────
2. Decision Logic Using the “Graph of Mappings” (Sharing and Mutation)

• Exam–type question: Given that the mapping structure (from virtual pages through page tables up to the actual physical frames) forms a directed acyclic graph, how do you decide whether you need to perform a copy (i.e. copy on write) for a given vertex (mapping)?
 Problem: When a write is requested on a shared mapping, what conditions dictate that you must “split” the state (i.e. duplicate the underlying physical frame and possibly update upper levels such as page table pages or the page directory)?
 Professor’s explanation and answer:
  – The decision is twofold:
   a. Do you want to mutate (i.e. write to) that particular vertex?
   b. Is the vertex shared (as determined by whether there’s more than one unique path pointing to it—effectively a reference count greater than one)?
  – Only if both conditions hold do you need to create a separate copy.
  – This even “back propagates”: if a page table entry is changed because of a split, its containing page table page or even the page directory may need to be duplicated if they are shared.
  Your exam answer should mention that you can use reference counting on the mapping graph to decide whether a copy on write is necessary.

──────────────────────────────
3. Logical vs. Physical Permission Bits in Copy‐on‐Write

• Exam–type question: What is the role of the logical permission bits (that control whether a process “should be allowed” to access an address) versus the physical permission bits (that actually determine whether the CPU will allow a write) in a copy‐on‐write system?  
 Problem: How can it be that two processes are logically allowed write access to a virtual address but physically prevented from doing so?
 Professor’s explanation and answer:
  – The logical permission bits indicate at a software (or OS) level that the virtual address is within a valid, writable region.
  – The physical permission (write) bit is cleared (set to 0) so that if a write is attempted to a shared physical frame, a trap occurs.
  – This trap allows the system to interpose and do the “deja vu” trick—i.e. it copies the underlying data to a new physical frame, updates the mapping (and back-propagates that update through the page table or page directory as necessary), and then restores physical permission.
  – This separation of logical versus physical permission is fundamental and was emphasized as a “big idea” in the lecture.
  Remember for exam: you may be asked to explain why this two-level permission mechanism is necessary for safe copy-on-write.

──────────────────────────────
4. Lazy Allocation and Demand Paging

• Exam–type question: Explain what lazy (or on-demand) allocation means in this context and why it is used.
 Problem: When an application requests multiple pages of memory, is it necessary to allocate all corresponding physical frames immediately? If not, how can lazy allocation help?
 Professor’s explanation and answer:
  – Instead of immediately allocating a separate physical frame for every requested virtual page, the system may allocate a single “special” frame or just mark the pages as not yet mapped.
  – Only when the application actually performs a write (or when memory is accessed in a demanding way) does the system allocate a proper physical frame.
  – This effectively “defers” heavy operations until more information about the process’s actual behavior is known.
  – This is the essence of demand paging, which helps oversubscribe physical resources.
  Your answer for an exam should emphasize that lazy allocation reduces upfront costs and can conserve memory when many allocated pages are never actually written.

──────────────────────────────
5. Impact of Function Calls on Page Directory/Page Table Mutations

• Exam–type question: What is the likelihood that a process will induce a mutation that requires copying (e.g., of the page directory) when making a function call?  
 Problem: When a process calls a function (for example, to work on its stack), what is the likelihood that this action will trigger copy-on-write on upper-level data structures?
 Professor’s explanation and answer:
  – A function call typically involves writing to the stack.
  – Even if the process is mostly reading in other segments, a call that modifies stack data will trigger a write.
  – This write eventually “backs up” into the page table (and even the page directory) if those structures were shared.
  – Hence, the probability of needing to duplicate (or “copy on write”) the page directory is extremely high—almost guaranteed for any process that invokes functions.
  Remember for exam: distinguish between the high probability of page directory mutations (because of stack writes) versus the workload-dependent probability of duplicating page table pages.

──────────────────────────────
6. Lab Two “Scope”: Which Components Must Be Handled for Copy-on-Write?

• Exam–type detail (also a lab hint): In lab two you are asked to implement copy-and-write—but note which parts of the paging data structures are in scope.
 Problem: For your lab, do you need to implement copy-on-write for page directories and page table pages or only for physical frames?
 Professor’s clear answer:
  – In lab two, you do NOT need to implement copy-and-write for the page directory and page table pages.
  – You only need to implement it for the last-level physical frames.
  – This is an important constraint so that you don’t get bogged down in an overly complex implementation.
  For the exam you may be asked to explain the trade-offs of copying versus not copying the higher-level structures.

──────────────────────────────
Additional Emphasis

• Throughout the lecture, the professor stresses how every “limitation” (e.g. XV6’s restriction that a physical page can only map once) is also an opportunity for system improvement.  
 – He uses concrete examples (e.g. mapping shared libraries to avoid duplication) to illustrate why multiple virtual addresses pointing to one physical frame are required.
 – Remember that every time the professor said “if I were to ask you this on the exam” or “on a test,” it indicates an exam–tip question that you should study.
 – He also emphasizes that many design decisions (lazy vs. eager copy on write) depend on the statistical properties of a workload—a point that could be turned into an exam essay or discussion question.

──────────────────────────────
Summary

Focus your studies on these key ideas:
 • How copying is deferred until a write actually occurs (copy-on-write mechanism).
 • The graph–model of mappings and the criteria (mutation + sharing) that force duplication.
 • The dual roles of logical and physical permissions in enforcing safe memory sharing.
 • The cost–benefit trade-offs between immediate copying versus lazy (on-demand) allocation.
 • The concrete lab constraint: only implement copy-on-write for physical frames (not for page directories or page tables).

Make sure you understand the professor’s line of thinking (deriving everything from first principles) and why each “design point” is important. Use these examples to practice solving problems as if they were on your exam.