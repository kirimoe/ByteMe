# About This Dataset

Dataset posted on 2023-03-15, 00:09 authored by Irfan Yousuf

A dataset for Windows Portable Executable Samples with four feature sets. It contains four CSV files, one CSV file per feature set. 

1.  First feature set (DLLs_Imported.csv file) contains the DLLs imported by each malware family. The first column contains SHA256 values, second column contains the label or family type of the malware while the remaining columns list the names of imported DLLs. 

2.  Second feature set (API_Functions.csv files) contains the API functions called by these malware alongwith their SHA256 hash values and labels. 

3.  Third feature set (PE_Header.csv) contains values of 52 fields of PE header. All the fields are labelled in the CSV file. 

4.  Fourth feature set (PE_Section.csv file) contains 9 field values of 10 different PE sections. All the fields are labelled in the CSV file. 



Malware Type / family Labels:

 

0=Benign

1=RedLineStealer

2= Downloader    

3=RAT

4=BankingTrojan

5=SnakeKeyLogger

6=Spyware

Paper:
```
@article{yousuf2023windows,
  title={Windows malware detection based on static analysis with multiple features},
  author={Yousuf, Muhammad Irfan and Anwer, Izza and Riasat, Ayesha and Zia, Khawaja Tahir and Kim, Suhyun},
  journal={PeerJ Computer Science},
  volume={9},
  pages={e1319},
  year={2023},
  publisher={PeerJ Inc.}
}
```