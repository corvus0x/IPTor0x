# IPTor0x

## Description
IPTor0x is a Python script that analyzes a list of IP addresses and determines which ones are TOR exit nodes. The results are displayed in the terminal and saved in an HTML report with a professional design.

<p align="center">
<img src=https://imgur.com/oIPfL9f.png>
</p>


## Features
- Checks if an IP is a TOR exit node by querying the official TOR exit list.
- Processes large lists of IPs efficiently using multithreading.
- Generates a detailed HTML report with categorized results.
- Displays results in a terminal output.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install requests jinja2 colorama
```

## Usage
1. Create a file named `IPs.txt` and add the list of IP addresses (one per line).
2. Run the script:

```bash
python IPTor0x.py
```

3. The results will be displayed in the terminal, and an HTML report will be generated (`tor_report.html`).


## Example
### HTML:

The script generates a tor_report.html file containing the analysis results. 


<p align="center">
<img src=https://imgur.com/3B1LnLS.png>
<img src=https://imgur.com/VEpBbSg.png>
</p>

## Contributions
If you want to improve the script or add new features, feel free to contribute! Fork the repository and submit a pull request.

## Author
Developed by corvus0x.

## License
This project is licensed under the MIT License. You are free to use and modify it as needed.
