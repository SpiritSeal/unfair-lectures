Below is a detailed list of the lecture segments—together with the “problems” (or thought‐exercises) the Professor sketched and his explanations—that appear to be flagged as potential exam questions. (Wherever the Professor said things like “if I were to ask you on the exam” or “this is a practice exam question,” I’ve noted those explicitly.) You can use these notes to review the concrete examples that might show up on your exam.

─────────────────────────────  
1. Ordered Write Operations & Crash Consistency  
─────────────────────────────  
• Problem sketch (from about the middle of the lecture):  
 “Let’s say you have three data blocks that you want to write. As you write them, you need to update your free block list data structure on disk and then persist your inode changes. In that precise order you write the data blocks, then update the free block list, and then write the inode (logged in the journal).  
 If these operations are not atomic and if, say, the metadata (inode update) becomes visible before the data blocks are safely written, you might end up with pointers that refer to blocks that haven’t actually been updated.  
 Imagine a crash occurs half–way through so that a metadata update is committed but the actual data isn’t on disk.”  

• Professor’s solution/explanation:  
 He explains that by enforcing the “write data before log metadata” ordering and then “flushing” before committing the metadata update, you guarantee that once the commit is visible (i.e. that group commit is made durable) both the data and the metadata become visible together. This “all or nothing” property is the crux of crash consistency in an ordered journaling system.  
 Important note: The Professor emphasized that “if the commit is visible to the external world, it must be true that the metadata is also visible” (enforced by flush) and that the data write happens first—even if a disk may reorder operations, the flush guarantees the ordering from a consistency point of view.

─────────────────────────────  
2. The Userspace “Atomic File Update” with a Log (Pseudo-code Example)  
─────────────────────────────  
• Problem sketch (near the latter part of the lecture):  
 The Professor describes a pseudo-code pattern for updating a file in user space using only POSIX operations. The “recipe” goes as follows:  
  – Create a log file in userspace  
  – Write the updates (with an accompanying checksum) into the log  
  – Write the actual update to the file  
  – Delete (unlink) the log file  
 He then poses the question (almost like an exam question):  
 “If I give you this pseudo-code on exam two and I ask you, ‘Have you persisted the file?’ what is the true/false answer?”  

• Professor’s solution/explanation:  
 He makes it clear that simply writing the file and deleting the log is not sufficient to guarantee persistence. In his explanation he points out that because the log file was created inside a directory, the directory’s metadata (the directory entry, or “dentry”) was changed.  
 Thus, you must also perform an Fsync on the directory to ensure that the new log file’s creation (and later, its deletion) are permanently recorded. In total, he shows that you need four Fsync calls (one for writing to the log, one for writing the file data, one for the directory update when creating the log, and one for the directory update when unlinking it) to guarantee atomic persistence.  
 He stresses that “if I give you this pseudo-code on exam two … you should be very, very confident that the answer is ‘No’ because more fsyncs are needed.”

─────────────────────────────  
3. GCC Compilation Metadata Update Thought Exercise  
─────────────────────────────  
• Problem sketch (roughly in the middle-to-late part of the lecture):  
 The Professor mentions GCC compilation as a motivating “exam–type” example when discussing metadata updates. He says something like:  
 “Think about GCC compilation on a Linux filesystem. During compilation, many very small files are created. What metadata updates would you expect to occur?”  
 He does not give a full list but hints that you must reason out which metadata updates would be performed (e.g. creating new inodes, inserting directory entries, allocating blocks, etc.). He also hints that these small metadata changes can experience head-of-line blocking if they are delayed behind large data updates in the log.

• Professor’s solution/explanation:  
 Even though he leaves this as a thought exercise, the intended answers include the fact that file–creation operations update the directory inode (by adding a dentry), allocate a fresh inode for each new file, and possibly update free block lists.  
 This example is important because he explicitly says, “this is like an exam type of question” and that you should think about all the possible metadata updates during compilation.

─────────────────────────────  
4. Fsync, Log Merges, and Ordering Across Files  
─────────────────────────────  
• Problem sketch (about two thirds into the lecture):  
 In a section discussing the performance implications of sequential logging, the Professor uses an example with two files. He outlines a scenario:  
  – There are two files, F1 and F2.  
  – You perform two writes on file F1 and one write on file F2.  
  – Then you call Fsync on file F2.  
 The question is: “What happens in the log and how does this Fsync interact with the ordering of pending writes from both files?”

• Professor’s solution/explanation:  
 He explains that Fsync on file F2 forces a dependency on its commit (labeled C2 in his diagram). But because the log enforces a global sequential order, this Fsync forces all preceding log entries (including operations from file F1) to be merged (or, effectively, flushed) to disk even if they aren’t strictly related to file F2.  
 This example shows that the Fsync triggers a “prefix merge” of the log, which is a performance penalty and is an ordering side–effect of using a single log for all filesystem operations.  
 This is flagged as an exam highlight because understanding this side effect is critical for explaining the tradeoffs in journaled file systems.

─────────────────────────────  
5. The Distinction Between Flush and Fsync  
─────────────────────────────  
• Problem sketch (discussed near the end and reiterated during the Q&A):  
 The Professor asks: “What’s the difference between issuing a flush and performing an Fsync?”  
 He notes that flush is used as a lower–level ordering primitive (ensuring that pending writes in the disk driver are executed before further operations are issued), whereas Fsync is a higher–level operation that guarantees a given file’s durability (by ensuring that all its updates, including those of related directory metadata, are permanently written to disk).

• Professor’s solution/explanation:  
 He makes the point that flush helps enforce a “happens–before” relation (for instance, ensuring that the data write happens before the commit write), but by itself does not guarantee file–level durability.  
 Fsync, in contrast, imposes both the ordering and the durability guarantees at the level of the file system interface.  
 This distinction is important both conceptually and for exam questions where you might be asked to explain or compare these primitives.

─────────────────────────────  
Additional Note – Tradeoff Diagram  
─────────────────────────────  
• In the very last part of the lecture, the Professor quickly reviewed a tradeoff diagram comparing fully journaled file systems, ordered file systems, and a write–back configuration with no journaling.  
• While no full “problem” was given, he pointed out that “the fully journaled solution gives maximum safety at a high performance cost, whereas ordering (or no journaling) can offer better performance with reduced safety guarantees.”  
• This comparison could easily be turned into an exam question asking you to explain the tradeoffs and to argue why certain operations (like Fsync calls) are used in one approach but not in another.

─────────────────────────────  
Summary  
─────────────────────────────  
Each of these examples illustrates not just how file system operations are ordered and persisted but also hints at the kinds of “if I asked you on the exam” questions you might encounter. The Professor stresses careful attention to the ordering guarantees (using flushes, commits, and fsyncs) and the performance implications of these designs, so make sure you are comfortable re–creating these examples and explaining the design tradeoffs from first principles.

Use these notes to review and work through each example until you can confidently reconstruct both the “problem” (the scenario put forth) and the “solution” (the ordering and consistency guarantees provided by the mechanism). Good luck studying!