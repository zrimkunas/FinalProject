# FinalProject

________________________
Product Biography/Readme
________________________

NoticeReporter.exe is a computer program that processes an office action from the United States Patent and Trademark Office using ChatGPT to generate a notice reporting letter for the office action. 

First things first, here are links to my deliverables:
* Pitch Deck: https://github.com/zrimkunas/FinalProject/blob/main/Pitch%20Deck.pptx
* User Testing Feedback:
* Final Technical Solution (Microsoft Windows): https://github.com/zrimkunas/FinalProject/blob/main/NoticeReporter.exe
* Source Code: https://github.com/zrimkunas/FinalProject/blob/main/main.py
* Test Data (Office Actions): https://github.com/zrimkunas/FinalProject/tree/main/OfficeActions
* Partner Letter: https://github.com/zrimkunas/FinalProject/blob/main/Partner%20Letter.pdf
* Solution Documentation (see below)
* Project Biography (see below)

________________________
How to Use the Software
________________________

In its current form, the software is an executable file that, when run, pops up a file selection dialog. The user need only browse to and select the office action they want analyzed and press ‘Ok.’ The software then works with ChatGPT to generate notice reporting text, which is provided to the user in a .txt file that pops up upon completion.
 
To execute the software:

1)    Double-click on the NoticeReporter.exe file. A file selection dialog will appear.

2)    Select an office action for reporting using the file selection dialog and press ok.

3)    Wait until the notice reporting text appears.
 

An attorney should always verify the notice reporting text before it is sent to the client.

________________________
Background
________________________

Patent Prosecution Law firms interface with the United States Patent and Trademark Office (USPTO) to obtain patent protection for their clients’ inventions. Most of the interaction between the firms and the USPTO is done in writing—the USPTO sends a document called an “office action” to the firm explaining why an invention isn’t patentable and the attorneys at the firm respond by amending the application or arguing that the USPTO’s assessment is wrong. 
 
The deadlines for responding to office actions are tight, so it is important that the client is promptly informed of receipt of the office action. This is accomplished by sending the client a “notice reporting” letter that briefly summarizes the contents of the office action and informs them of the deadline for responding.
 
Notice reporting letters are easy for patent attorneys to write, but they are seen as busy work that is too expensive to bill clients for. So, the task falls to paralegals and administrators, who don’t necessarily have the experience to understand and summarize the contents of the office action. 
 
________________________
Status Quo
________________________
 
The status quo is that paralegals and administrators attempt to draft a notice reporting letter and provide their attempt to the responsible attorney. The responsible attorney then corrects any mistakes in the letter before it is sent out. The entire process probably takes about an hour. But it really should be quick because drafting notice reporting is somewhat formulaic if you know what you’re looking for. 
 
________________________
Previous Attempts
________________________
 
I’ve previously attempted to make a template notice reporting letter in Microsoft Word that used menus to guide paralegals and administrators in drafting notice reporting letters. The attorneys loved the template but the paralegals and administrators found it confusing and hated it—they vetoed using it.
 
I then attempted to use regular expressions to automatically parse office actions. That didn’t work well because, while office actions are somewhat structured, they aren’t structured enough to enable the use of regular expressions.
 
________________________
This Software
________________________
 
This software uses ChatGPT to parse a USPTO office action to generate a notice reporting letter (i.e., document automation and data scraping). The software provides certain sections of the office action to ChatGPT and asks questions about those sections such as:
-is the office action a non-final office action or a final office action?
-what is the response deadline?
-are there any claim objections?
-and so on….
 
The answers to those questions are then used to construct the text of the notice reporting letter. 

____________________________________________________________
Limitations of Current Implementation
____________________________________________________________
 
-       The current implementation only works with .pdf versions of office actions that have been OCR’ed (i.e., have selectable text).

-       The current implementation is only designed to generate notice reporting letters for non-final and final office actions issued by the U.S. Patent Office. 

-       There are certain types of office actions that require attorney input. Those types of actions are flagged by the software.

-       The current implementation is not pretty.

-       The current implementation doesn’t have any error handling.

-       The current implementation is somewhat slow.


________________________
Complexity/Robustness
________________________
This project makes extensive use of ChatGPT in a document scraping and automation task. It is implemented in the Python Programming language. The Python programming aspect of the project was fairly easy, but the prompt engineering was almost maddening—it’s much more complex than I expected. 

________________________
User  Testing
________________________

As a first testing step, I volunteered to show a working prototype of the software to the firm at our firm meeting. Thankfully, the prototype worked and the firm was able to see an example of an automatically generated notice reporting letter. The attorneys and paralegals in the meeting noted certain features (e.g., identification of the type of office action--non-final or final) that would be desirable in a final prodcut. After that meeting, I augmented the software based on the feedback I received. Among other features, the updated version of the software was able to determine and indicate office action type in the notice reporting letter. 

For a second testing step, a paralegal and an administrator from my firm volunteered to test this software for me. The paralegal is our lead paralegal, an experienced professional with over 15 years of experience as a patent parealegal/secretary. She is an expert. Our administrator is a smart entry level employee who is learning the ropes of the patent business. 

I provided them with the executable and a set of OCR’d office actions that we had previously received from the USPTO. I also provided them with a feedback form. Their completed feedback forms. I have sent the completed feedback froms to Professor Colarusso. 

Their feedback indicated that the software provided almost entirely correct information (with a few exceptions), but that they would be more likely to use the software if it had certain additional features that are beyond the scope of this product. I am optimistic that I will have support from our staff to continue development of this software to make a product that our team is willing to use.


If you want to test the software, download the executable and the test data:
* Final Technical Solution (Microsoft Windows): https://github.com/zrimkunas/FinalProject/blob/main/NoticeReporter.exe
* Test Data (Office Actions): https://github.com/zrimkunas/FinalProject/tree/main/OfficeActions
  
________________________
Refinement
________________________
As is noted above, the software was refined based on feedback received in a firm-wide show-and-tell. In general, the feedback I continue to receive is that people want the software to be more full-featured. All the refinements I've done so far have been to increase the features of the software and the feedback I still need to address is more of the same. 

Surprisingly, the paralegals and administrators in my firm seem to like the functionality of the software and support further refinement and implementation in their workflows. 

________________________
Impact & Efficiencies
________________________

All in all, the software takes about a minute to construct a notice reporting letter. This is 1/60th of the combined time it presently takes paralegals+administrators+attorneys to draft a notice reporting letter.

________________________
Fit/Completeness
________________________

A fully complete solution would be too big a task for a school project. However, the current state of the software is able to draft notice reporting letters for about 80% of the office actions that we receive from the USPTO. While the UI is simple, I think it’s very intuitive given the simplicity of the task. 

Paralegals and administrators are creatures of habit, so it might take some time to convince them to use the software. But I do believe it is a great improvement over the status quo. 

________________________
Real World Viability
________________________

As mentioned above, this is an 80% solution. I have presented this product to our firm at a firm meeting and the hope is that the paralegals and administrators will begin using it now.

Here’s what is left to do:

	-Automatic OCR’ing of pdfs.
 
	-Handling of certain edge cases (e.g., all claims allowed).
 
	-Improved UI
 
	-Batch processing of office actions
 
	-Present text in an email (instead of .txt file).
 
	-Error handling

________________________
Sustainability
________________________

One of the partners has a son with a computer science degree. The son can’t find a job so there is a possibility that he will pick this project up where I left off and make it into a more robust and full-featured program. But to be successful, I really need to gain the trust of the end-users (i.e., the paralegals and admins).

I’m curious about whether we should switch away from ChatGPT to something like huggingface soon because ChatGPT is slow and the API costs money. That’s a possible next step.

 
