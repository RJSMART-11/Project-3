# Project 3, Group 1
**Blockchain Election Voting System**

-----------------------------------------
**Introduction**

This project is the creation of a election platform driven by blockchain technology to provide shareholders with a secure, real time, corruption-free process.

It combines blockchain technology with a Streamlit user interface and has been designed to simplify the user experience as much as possible, whilst ensuring a robust , transparent and effective system.

------------------------------------------
**Technologies used**

- Solidity: used to create the smart contract and execute the blockchain transactions
- Remix IDE: enabled the compiling and editing of the Solidity code and the is the application where the code is run
- OpenZepplin: library for ERC20 conrtacts
- Ganache: to provide pre funded etherum accounts and transactions
- Web3: to deploy the blockchain contract
- Streamlit: enable an application in a web browser to provide interaction with the ledger, or simply put - to create a user friendly interface and run the voting process
- Python: coding environment for the pages of the Streamlit application
- Visual Studio: coding envirnment for Streamlit application
- Metamask: as the wallet environment to interact with Ganache

To see all libraries and dependencies please refer to individual working files in the above folders.

-------------------------------------------
**Solution Overview**

The system enables one vote per candidate by each person voting. The process from the user has been kept as easy and simple as possible to ensure easy compliance and remove any barriers to accepting the technology and using the system.

In practice the process would be:
a) user is provide with a secure link via email or message service
b) once accessed the site provides information on the purpose and process, candidates and real time status of the campaign
c) the voter is required to verify their identity via a one-time-password (OTP)
d) the OTP enables access to select a candidate and cast a vote
e) prior to casting the vote a visual record, photograph, of the voter is captured by the system
d) once cast the vote is recorded by the blockchain and passed to the system to update the progress of the poll

To operate the system:

1. Install Metamask and create an account
2. Install the Ganache Truffle Suite on your desktop
3. Open Remix IDE and open the election.sol file
4. Compile and run the process
5. Deploy the contract in in the 'injected Web3' environment
6. Update the Env and python files wallet address and Web3.HTTPProvider to your specific needs
7. Launch terminal and open the voting.py and Election_Home.py files in the folders above in the Streamlit application 
8. To view the election process user interface please go to the instructional video video : https://vimeo.com/796145039

-------------------------------------------
**Future Developments**

The current platform has the capacity to evolve to include:

1.  User verification against a unique database. 
    This would include features to upload a database record of 'voters' to the blockchain that confirms their 
    identity as an option to requiring an OTP

2.  Providing voters with an number of tokens that reflects their shareholder/status rights, or allows voting across a range of issues:
    a) allows voters to place greater weight their choice of candidate/issue based on their voting rights
    b) provides voters with the ability to vote across a panel of candidates/issues
    
3.  Database of all transactions including visual or other verification
-------------------------------------------
**Contributors**

To discuss this project or the potential for future development please contact:

Robert Smart: robertjonathonsmart@gmail.com
Karin Halpin: karin_halpin@yahoo.com.au
Danny Milsom: dannymilsom@y7mail.com
Illia Parkhomenko: john1996st@gmail.com
Brendan van Maanen: vanmaanen.brendan@gmail.com
