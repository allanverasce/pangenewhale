<p align="center">
  <img src="screenshots/logo.png" alt="Logo" width="300" height="300" />
</p>

# From Benchmarking to Application: PanGeneWhale, a User-Friendly Platform for Pangenomic Analysis
<p align="justify">The choice of software for pan-genomic analysis is challenging due to barriers such as usability, performance, complexity, and the diversity of available solutions. These issues often require advanced knowledge and compromise reproducibility. To explore this scenario, we conducted a comprehensive benchmarking of 12 tools applied to 50 <em>Escherichia coli</em> genomes. The analysis revealed significant disparities in computational performance (CPU, memory, and storage usage) and in the biological composition of the generated pangenomes. Critical usability barriers were also identified, including outdated dependencies and a lack of graphical interfaces. To overcome these limitations, the benchmarking motivated the development of PanGeneWhale, a platform that integrates the evaluated solutions in a containerized environment (Docker). With an intuitive, cross-platform graphical interface, the software automates execution flows, ensures reproducibility, and broadens access to pan-genomic analysis. Thus, it represents a solution that supports both researchers with limited computing experience and advanced users, simplifying the conduct of large-scale studies.</p>

### Technology
<image src="https://github.com/allanverasce/allanverasce/assets/25986290/e9eef5db-3d9e-419d-bc31-c29c16076146" alt="Image" width="50"/>
<image src="https://github.com/user-attachments/assets/3406d50a-a37b-4980-976f-61d0cf916957" alt="Image" width="50" />
<image src="https://github.com/user-attachments/assets/b1cb9cb4-33f1-4069-8c0b-078dbf994847" alt="Image" width="50" />
<image src="https://github.com/user-attachments/assets/5b44250e-ced9-46a6-84dd-a4954f408495" alt="Image" width="50" />

### Compatible with:
<image src="https://github.com/allanverasce/allanverasce/assets/25986290/3f178481-786d-4e6f-b46f-7e10732e9ca8" alt="Image" width="50"/>
<image src="https://github.com/user-attachments/assets/3ba215a2-9849-4e21-a84c-e7e32bdc19aa" alt="Image" width="50" />
<image src="https://github.com/user-attachments/assets/97a4af37-07f2-4283-ae7d-9a1db3e51d50" alt="Image" width="50"/>


# Installation and User Guide 

Before using PanGeneWhale, it is necessary to ensure that all required dependencies are properly installed. This section provides an overview of the software and libraries that must be set up in advance, allowing the tool to run smoothly and without compatibility issues.

### Dependencies
- To use PanGeneWhale, it is required to have Docker installed on your operating system. Docker provides the containerized environment necessary to run PanGeneWhale. You can find the official instructions and download them at: `https://docs.docker.com/engine/install`
- You need to install Java if you want to run it using the JAR package. To use this option, the user must have Java 17 previously installed on their system. The official Java 17 package can be downloaded from: `https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html`
  

# 1. PanGeneWhale installation on Windows
To begin with, check that you have this software installed on your device:

```bash
git - https://git-scm.com/downloads/win
java version 17 
```
1.1. To start the installation, let's clone the repository with the git clone command and the correct URL in the desired folder.</br>
1.2. At the end, enter the folder of the cloned repository you just cloned, in this example, PanGeneWhale.


# 2. Installing PanGeneWhale on Linux. How to use Java package?
LINUX (Debian 12 e 13): To install using the standard .deb package, follow the model below. Run the line on your Linux terminal 

```bash
apt install ./pangenewhale.deb
```

To run using the JAR package. Open the terminal and run using JAVA, following the example below:

```bash
java -jar pangenewhale.jar
```

# 3. Executing PanGeneWhale
When you start the application, you will see the presentation screen. Here, the user will find a brief description of the software. To access more information, simply click on the "Learn More" button. On this same screen, all previously created projects are listed. The user can:

* View details of previous projects.
* Reuse existing projects for reprocessing with already configured parameters;
* Delete projects that are no longer needed.
* You can also start a new workflow by clicking on “Create New Project”

<img src="screenshots/mainWin.png" alt="Main" width="800" height="600" /> 
