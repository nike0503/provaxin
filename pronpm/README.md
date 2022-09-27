1. Clone [this repo](https://github.com/HynekPetrak/malware-jail) and note the absolute path of the directory.

2. Edit [core/config.js](https://github.com/nike0503/provaxin/blob/main/pronpm/core/config.js) and update the absolute paths of the pronpm directory (which should probably be the directory of this readme file), and the malware-jail directory (as was noted in step 1)

3. Install the dependencies

```
cd core && npm install
cd .. 
cd pefile-model && pip -r requirements.txt
cd ..
```

4. In the pronpm directory, test the pronpm tool as follows:

   * Run ```chmod +x ./pronpm``` to allow the pronpm script to become executable.

   * Sample 1: An actual malware collected from an internet dataset. Try: 
   
     `./pronpm install dryairship/provaxin-samples#sample1`

   * Sample 2: A very simple benign file: Try: 
   
     `./pronpm install dryairship/provaxin-samples#sample2`

   * Sample 3: A malicious package that downloads one malicious and one benign file from the internet. Try: 
   
     `./pronpm install dryairship/provaxin-samples#sample3`

   * Sample 4: A benign package that downloads one benign file from the internet. Try: 
   
     `./pronpm install dryairship/provaxin-samples#sample4`

