# CompSuite
CompSuite is the first incompatibility issue dataset focusing on library behavioral incompatibility with concrete reproducible test cases. 

## Install
You can clone the repository to your local environment. Here we provide our operating environment for reference (Java 1.8; Maven 3.6.3; Python 3.11).
```bash
    git clone https://github.com/compsuite-team/compsuite
```

## Get Started
Get into compsuite folder and you will find main.py and relevant files. All incompatibilities with unique ID are saved in incompatibilities.json. Then, you can use following commands to use CompSuite. 

### 1. incompat
Following command will assist users to download and compile target client, then checkout to base version with old tag and run test first. Next, CompSuite will checkout to incompatible version with new tag and re-run the same test.
```bash
    python main.py --incompat [id]
```

### 2. info
Check detailed information of incompatibility.
```bash
    python main.py --info [id]
```

### 3. download
Download target client.
```bash
    python main.py --download [id]
```

### 4. compile
Compile target client.
```bash
    python main.py --compile [id]
```

### 5. test
Execute test at base version and incompatible version.
```bash
    python main.py --testold [id]
    python main.py --testmew [id]
```

## Reference
If you would like to use CompSuite in your research, please cite our paper.
```
@misc{xu2023compsuite,
      title={CompSuite: A Dataset of Java Library Upgrade Incompatibility Issues}, 
      author={Xiufeng Xu and Chenguang Zhu and Yi Li},
      year={2023},
      eprint={2305.08671},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```
