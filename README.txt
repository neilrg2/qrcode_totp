**************************************************************************************

Before beginning, there is a library that is not standard with Python that needs to be 
downloaded. This library is called 'qrcode' which performs the QR Code JPG generation.
This is the only dependency that needs to be installed. The rest of the libraries used 
are standard with Python. I will outline how to go about installing it below.

This program is written in Python. The version of Python used is Python 3

**************************************************************************************
    
    1) Windows
    2) Linux/UNIX

For Windows & Linux/UNIX, make sure to have a version of Python 3 installed. If not make sure to install
Python via their official website for your platform.

Also ensure you have pip installed. With most versions of Python it comes with the Python installation. If 
not, make sure to download pip as well.


Linux/UNIX:
    Perform the below steps via terminal/command line.

    Check to see you have the latest version of pip:

        python3 -m pip install --user --upgrade pip

    Install 'qrcode' & 'Image' packages:

        python3 -m pip install --user qrcode
        python3 -m pip install --user Image

    
    Once you have a version of Python 3, pip, qrcode & Image libraries installed, 
    you are ready to run the program.

    
Windows:
    Perform the below steps via command prompt. (NOTE: Ensure Python was added to your PATH. If fresh 
    install, there is an option during installation to add it)

    Check to see you have the latest version of pip:

        py -m pip install --upgrade pip

    Install 'qrcode' & 'Image' packages:

        py -m pip install --user qrcode
        py -m pip install --user Image

    
    Once you have a version of Python 3, pip, qrcode & Image libraries installed, 
    you are ready to run the program.


**************************************************************************************

Linux/UNIX:

    Type the command below to generate QR code:

        python3 submission.py --generate-qr

Windows:

    Type the command below to generate QR code:

        py submission.py --generate-qr


Once that is completed, it is now time to generate the TOTP with my program. I implemented the program
to continue generating every 30 seconds and running forever. A keyboard interrupt has to be sent
to terminate the program. The --get-otp command is implemented in a way to generate the TOTP as close
in sync with the GA App code generation as possible time-wise.

Linux/UNIX:

    Type command:

        python3 submission.py --get-otp

Windows:

    Type command:

        py submission.py --get-otp



At this point, that is the program! NOTE: The secret key used is hard-coded.

**************************************************************************************