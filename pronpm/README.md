Clone [this repo](https://github.com/HynekPetrak/malware-jail) and note the absolute path of the directory.

Edit provaxin/pronpm/core/config.js and update the absolute paths of the pronpm directory (which should probably be the directory of this readme file), and the malware-jail directory (as was noted in step 1)

cd into provaxin/pronpm/core and run "npm install" to install the dependencies.

cd into provaxin/pronpm/pefile-model and run "pip -r requirements.txt" to install the dependencies.

cd into provaxin/pronpm and test the pronpm tool as follows:

Run 
```chmod +x ./pronpm``` to allow the pronpm script to become executable.

5.2. Sample 1: An actual malware collected from an internet dataset. Try: `./pronpm install dryairship/provaxin-samples#sample1`

5.3. Sample 2: A very simple benign file: Try: `./pronpm install dryairship/provaxin-samples#sample2`

5.4. Sample 3: A malicious package that downloads one malicious and one benign file from the internet. Try: `./pronpm install dryairship/provaxin-samples#sample3`

5.5. Sample 4: A benign package that downloads one benign file from the internet. Try: `./pronpm install dryairship/provaxin-samples#sample4`

