### 1. Complexity of fork in vanilla Unix V6 and optimization with copy-on-write
**Key Points**
- Fork performs a full copy of all physical frames of the parent's virtual address space.
- Complexity of fork in this vanilla approach is **O(N)**, where N is the number of physical frames.
- Copy-on-write optimization changes the complexity to **O(1)** by initially sharing physical frames between parent and child.
- Copying is deferred until a write actually occurs, using a lazy allocation mechanism.
- This optimization dramatically improves performance and is fundamental.

**Problem statement:**
What is the complexity of fork in vanilla Unix V6 as a function of the number of physical frames? How can we improve it using copy-on-write?

**Solution:**
- Vanilla fork is O(N) because it copies all physical frames.
- By using copy-on-write, instead of copying all frames immediately, the child’s virtual frames initially map to the same physical frames as the parent.
- This reduces complexity to O(1) because the operation no longer copies frames up front.
- Writes by the child trigger actual copying (copy-on-write), deferring the cost.
  
_Summary: This is a classic example given by the professor and flagged as "if I were to ask you this on the exam." Understanding the complexity change by using copy-on-write is fundamental._

---

### 2. Example of copy-on-write on write to stack after fork
**Key Points**
- After fork with copy-on-write, the child's stack (red frame) and other memory regions share physical frames with the parent.
- The child has logical write permission but no immediate physical write permission; the write bit in page table entry is set to zero.
- The write attempt triggers a trap to the kernel.
- The kernel copies the physical frame and updates the child's page table entry to point to the newly copied frame with write permission enabled.
  
**Problem statement:**
Explain what happens when the child process attempts to write to its stack frame (red frame) after fork with copy-on-write.

**Solution:**
- Initially, the child's stack page has the write bit set to zero (physical permission denied).
- When the child writes, a trap occurs because physical permission is lacking.
- The kernel copies the physical frame corresponding to the stack (red frame).
- The child's page table entry is updated to point to this new physical frame.
- The write bit in the child's page table entry is set to one to allow writing.
- The child can now write to its own stack without affecting the parent’s stack frame.

_Summary: Copy-on-write protects isolation by allowing logical permission (program can write) while deferring actual copying until the physical write happens. This example is explicitly walked through by the professor and is highly likely to be exam-relevant._

---

### 3. Permission bits and logical vs physical permissions distinction
**Key Points**
- Two types of permissions exist: logical (is write legal for the process?) and physical (does hardware allow the write?).
- The OS clears the physical write bit in the PTE to prevent writes and trigger traps.
- The kernel is omniscient and controls these bits, allowing it to interpose on processes.
- Physical write bits act as mechanismic controls to enable copy-on-write behavior.
  
_Summary: This conceptual distinction is fundamental for understanding copy-on-write. The professor emphasizes the importance of separating logical permission (program semantics) from physical permission (hardware protection with PTE bits)._

---

### 4. Recursive copy-on-write algorithm to handle page and page table copies
**Key Points**
- The process's mappings can be represented as a directed graph with vertices representing physical frames, page tables, page directories.
- When a write triggers copy-on-write, the affected physical frame is copied.
- If the page table containing the PTE must be mutated, it also must be copied if shared (more than one reference).
- This back-propagates to copying page directory entries similarly.
- The same "reference counting + graph traversal" logic applies recursively at every level.
- This supports complex process family hierarchies (children, grandchildren, etc.).

_Summary: The professor gives an explicit conceptual algorithm for multi-level copy-on-write involving page tables and directories represented as a graph with references. This recursive approach is crucial and likely to be exam-worthy._

---

### 5. Example: Copy-on-write permission bits after fork and write by child process
**Key Points**
- After fork:
  - All processes share same physical frames.
  - The kernel sets all write bits in PTEs to zero to prevent physical writes.
- When child process wants to write to a physical frame (e.g. P1):
  - Trap occurs.
  - The kernel copies the physical frame to P1'.
  - Updates child's page tables and directory to point to P1'.
  - Sets write bit for P1' PTE to 1 (write allowed).
- Write bits for other shared frames remain zero.
- Updates respect reference counts and mappings from the graph model.

_Summary: The professor carefully walks through this step-by-step example, connecting it to the earlier graph model and showing how permission bits are managed to support copy-on-write, emphasizing the necessity to handle all levels of the page table hierarchy. This detailed example is an ideal candidate for exam questions._

---

### 6. TLB invalidation after copy-on-write
**Key Points**
- When a page table entry changes (due to copy-on-write), corresponding entries in the TLB must be invalidated.
- Only one TLB invalidate is needed in the current process's context (process 2 in example).
- The parent process (process 1) still points to original P1 frame but has write bit zero to avoid unnecessary traps.
- The TLB for process 1 is flushed on context switch because CR3 register is loaded, which invalidates TLB.

**Problem statement:**
How many TLB invalidations are needed after performing a copy-on-write on physical frame P1 by the child process?

**Solution:**
- Exactly one TLB invalidate is performed for the child process (process 2).
- No immediate TLB invalidation is needed for the parent process (process 1) because the kernel will flush the TLB on context switch to process 1.
- This single TLB invalidate targets the updated PTE for P1' in the child's page tables.

_Summary: This is presented as a trick question and illustrates the importance of understanding TLB behavior in virtual memory. The professor explicitly discusses this and it should be well understood for the exam._

---

### 7. Lazy allocation and zero-filling optimization example
**Key Points**
- Virtual memory need not be fully populated with physical memory upfront.
- Supports oversubscription: allocating more virtual pages than physical pages.
- Physical pages can be zero-filled lazily on first write to save expensive zeroing operation on allocation.
- Example: malloc or sbrk calls defer physical allocation until page is written.
- Zero-fill avoids security issues (leaking previous data in reused frames).

**Problem statement:**
When a process calls sbrk to allocate 2 pages, what physical pages are assigned immediately, and how do we handle the zero-filling efficiently?

**Solution:**
- No physical pages are immediately allocated on the sbrk call.
- Both virtual pages are mapped to a single zero-filled physical page with read-only protection.
- On first write (copy-on-write), the page is copied and zero-filled lazily.
- This saves memory and CPU time by avoiding zeroing before actual writes happen.

_Summary: Lazy allocation and zero-filling are fundamental performance optimizations. The professor stresses always thinking about trade-offs here. This is important for exam questions related to demand paging._

---

### 8. Shared memory example with shared libraries mapping
**Key Points**
- Shared libraries provide a common shared memory mapping in virtual address space across processes.
- Physical frames corresponding to shared libraries are mapped read-only and shared among multiple processes.
- Saves significant memory as code pages are shared, not duplicated.
- Example given: two sleep processes sharing libc mapping in /proc/PID/maps.
- All mappings are page aligned (4KB page size).
- Mapping details reveal how many virtual frames and page tables map the shared library.
- Example calculating number of PTEs (0x18A) needed to map the code segment.
- Explains that a single page table page suffices because it holds 1024 entries.

**Problem statement:**
How many page table entries and page table pages are needed to maintain the mapping of a shared library code segment spanning 0x18A VFN?

**Solution:**
- Number of PTEs equals the number of pages in the range: 0x18A (~394 decimal).
- One page table page can hold 1024 entries.
- So, only one page table page is needed for the mapping.

_Summary: This concrete example ties virtual memory mapping details to real-world shared memory use cases and page table structures, useful for exam questions about shared memory and page table organization._

---

### 9. Takeaway/fundamental points emphasized by the professor (for exam relevance)
**Key Points**
- Precise meanings of "virtual frame number" (VFN), "physical frame number" (PFN), and mappings.
- Copy-on-write is crucial for performance—understand when and how copying happens.
- Logical permissions vs physical permissions distinction is fundamental.
- Permission bits at page table and page directory levels both matter.
- Conceptualize page tables and pages as a graph of references for copy-on-write.
- Lab 2 focuses on implementation details for copy-on-write and tracking sharing.
- TLB invalidations are tied to context and should be understood.
- Lazy allocation and zero-fill pages are key optimizations.
- Shared memory mappings save physical memory and are actively used (e.g., libraries).
- Understanding of page table sizes and entries—practical calculations.

---

# Summary

The lecture contains numerous exam-worthy examples and conceptual models:

- Complexity of fork and copy-on-write optimization (O(N) to O(1)).
- Detailed step-by-step copy-on-write example on child's stack write.
- Recursive graph-based approach to copying page tables and directories.
- Permission bit management and distinction between logical and physical permissions.
- TLB invalidation strategy after copy-on-write.
- Lazy allocation and zero-filling optimizations, especially related to sbrk/malloc.
- Shared memory mapping illustrated by shared libc segments and page table calculations.
- Realistic motivation of advanced research papers improving fork with page table copy-on-write.

These examples should be fully mastered by solving related problems from first principles, as the professor indicated most things can be derived that way. The concrete examples and the emphasis on permission bits and graph modeling are especially critical for exams and labs.