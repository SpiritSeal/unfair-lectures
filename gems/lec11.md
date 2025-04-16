### 1. Example of Kernel Code and Interrupt Handler accessing shared variable (Interrupt Deadlock Example)
**Key Points**
- Interrupts enable concurrency but create challenges when accessing shared variables.
- Both kernel code and interrupt handlers may lock the same shared variable.
- Without careful management, this can cause deadlock due to cyclic dependency on locks.
- The solution involves disabling interrupts during critical sections to establish *relative atomicity*.
- Atomicity is relative, not absolute, depending on the observer thread/execution.
- XV6 code uses disabling and enabling interrupts around spin lock acquire and release to prevent deadlocks.

**Problem statement:**
You have kernel code on the left writing to a shared variable, protected by a lock, and an interrupt handler on the right reading from the same shared variable. Both protect their access via locks. Is this code safe? If not, why? What can cause deadlock?

**Solution:**
- Answer: The code is *not* safe because the interrupt can occur while the kernel holds the lock, causing the interrupt handler to try acquiring the same lock.
- This causes a deadlock cycle: the interrupt handler waits on the kernel lock to release, but the kernel is paused in the critical section waiting for interrupts to complete.
- Solution: disable interrupts during the kernel's critical section, so the interrupt handler cannot interrupt and try to acquire the lock.
- This establishes *relative atomicity* across the kernel code and interrupt handler, instead of just mutual exclusion with locks alone.
- This is implemented by disabling interrupts when the lock is acquired and enabling them when the lock is released (as in XV6 spinlock implementation).

_Summary_: This example fundamentally demonstrates interrupt-driven deadlock and the necessity of interrupt disablement to achieve correct concurrency control in kernel code. Important foundational principle about atomicity being a *relative* concept between concurrent threads and interrupt handlers. Definitely exam-worthy.

---

### 2. The "Too Much Milk" problem (Classic concurrency example)
**Key Points**
- Introduces basic concurrency problems via real-world analogy: two roommates (Alice and Bob) want to buy milk if none is in the fridge.
- Problem arises when both check the fridge before either buys milk → both end up buying milk → too much milk.
- Two key correctness properties: **liveness** (milk must eventually be bought) and **safety** (at most one buys milk).
- Naive solutions like leaving notes fail because checking and writing notes are not atomic.
- The example motivates the need for atomic operations or concurrency primitives ensuring mutual exclusion.
- Mention of Peterson’s algorithm as a classical solution ensuring mutual exclusion in concurrent access without atomic exchange.
- Illustrates that atomic operations and hardware support are needed to build correct concurrency primitives.
  
**Problem statement:**
Bob and Alice both check an empty fridge for milk. If empty, each goes to the store and buys milk. Why does this lead to the problem of too much milk? What concurrency principle is violated? How can this be corrected?

**Solution:**
- Problem: Both check before either buys milk and thus both buy milk → violates the **safety** property (only one should buy).
- Leaving a note before buying milk doesn't solve the problem because note placement itself isn't atomic with the checking.
- Solution involves atomic primitives ensuring combined check-and-act steps happen atomically, like atomic exchange or Peterson’s algorithm.
- Introduce concurrency controls so that checking and updating fridge state happen atomically relative to other threads.

_Summary_: The "too much milk" example is a canonical concurrency problem that illustrates why simple checks and sequential thinking are insufficient in concurrent systems, motivating atomicity and proper synchronization. This example and its conceptual explanation are critical for exams.

---

### 3. Spinlock implementation using atomic exchange (Lock acquisition example)
**Key Points**
- Spinlocks are built using atomic exchange operations that atomically check and set lock state.
- Exchange attempts to set lock=1 and returns previous value atomically.
- If exchange returns 1 (lock held), thread spins (busy waits).
- If exchange returns 0 (lock free), thread acquires the lock.
- The lock implementation forms a finite state machine with 4 states based on lock and result variable.
- Successful acquisition corresponds to state where lock=1 and result=0.
- This is foundational for understanding low-level synchronization primitives in operating systems.
- Professor emphasizes that understanding these states and transitions can be exam questions.

**Problem statement:**
Show how an atomic exchange operation can be used to implement a spinlock's acquire function. What are the possible states of the lock and result? Which state indicates successful lock acquisition?

**Solution:**
- The acquire function sets result (R) to 1 and loops while R != 0.
- Inside the loop, exchange(lock,1) atomically swaps 1 into lock and returns previous lock value.
- If lock was held (1), exchange returns 1 → R remains 1 → loop continues.
- If lock was free (0), exchange returns 0 → R set to 0 → loop ends → lock acquired.
- The lock and R variables form four states: 
  - 00, 01, 10, 11
- Success state is 10: lock=1 (held), R=0 (successfully exited loop).
- States 11 and 01 correspond to trying to acquire or releasing, with spins in 11 waiting.

_Summary_: This concrete spinlock implementation with atomic exchange and finite state conceptualization is a key learning for understanding locking in OS kernels, and will likely appear on exams. Understanding the states and their meanings is fundamental.

---

### 4. Instruction reordering and memory model example (X86 total store order example)
**Key Points**
- Two threads execute instructions accessing shared variables X and Y.
- Different interleavings can produce results A, B, C, D, and even unexpected behaviors due to instruction reordering.
- X86 uses Total Store Order (TSO) memory model: stores are ordered, loads can be reordered.
- Compiler and processor may reorder instructions without data dependencies.
- Sequential consistency (SC) is not guaranteed unless code is data-race free (DRF).
- Understanding reads and writes ordering and hardware memory models is crucial.
- Professor says this example is "mind blowing" and highlights that all result combinations are possible.
- Important for understanding subtle behaviors in concurrent code and necessary use of synchronization.

**Problem statement:**
Given two threads with initial X=0, Y=0:
- T1: X=1; EAX=Y;
- T2: Y=1; EBX=X;
What are the possible values for EAX and EBX after concurrent execution? Why can all results (A through G on the slide) occur?

**Solution:**
- Due to instruction reordering by compiler/processor (no data flow dependencies), instructions can be executed in any order.
- Possible interleavings allow any combination of EAX and EBX to be 0 or 1, including unexpected results like 0,0.
- X86 memory model guarantees total store order on writes but not on loads, allowing loads to be reordered.
- Sequential consistency is only guaranteed if code is data race free, which this code is not.
- Thus all results are theoretically possible.

_Summary_: This example drives home the complexity of concurrent programming on real hardware due to weak memory models and instruction reorderings. Recognizing potential states and the implications of memory models is essential and likely an exam topic.

---

### Additional points mentioned with exam emphasis

- The professor specifically said: "This kind of stuff will be on the test" when explaining the atomic exchange spinlock behavior and state transitions.
- The finite state automaton reasoning for spinlock states is suggested as a possible exam question ("If I were to ask you...").
- Emphasis on understanding *relative atomicity*—that atomicity is dependent on perspective and concurrent entities.
- The "too much milk" problem and its formal safety and liveness definitions are fundamental for reasoning about concurrency correctness.
- The instruction reordering example is said to be "mind blowing" and the professor expects students to be able to explain all possible states and interleavings.
- The professor advised reviewing the XV6 code for interrupt disable/enable around spinlock acquire/release, indicating practical relevance for exams.

---

**Summary of the entire lecture's key exam-relevant examples:**

1. Kernel and Interrupt concurrency problem causing deadlock without disabling interrupts.
2. "Too much milk" example demonstrating safety vs liveness in concurrent updates.
3. Spinlock implemented via atomic exchange and understanding its finite state model.
4. Instruction reordering example illustrating weak memory models and possible unexpected states.

Each example illustrates fundamental concurrency challenges, requiring understanding of atomicity, mutual exclusion, memory ordering, and hardware support for concurrency primitives. All are marked or hinted as possible exam topics by repeated emphasis and framing by the professor.