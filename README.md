# Fine-tuned GODEL for tech support

[Microsoft GODEL](https://www.microsoft.com/en-us/research/project/godel/) is an open-source pre-trained language model for goal-directed dialogs that uses a Transformer-based encoder-decoder model. The documentation states that the model is effective at generating task-specific dialog for new tasks when fine-tuned on dialog specific to the new tasks. Hence, I decided to use this model for fine-tuning to create a tech support chat model.

Data used for fine-tuning was an open source dataset containing conversations on Twitter between customers and customer support accounts. ([Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter))

## Fine-tuning Documentation 
### Data Preprocessing
Conducted data preprocessing to ensure data is in the right format to be input into the model for training and ensure that text data is cleaned.
- Checked for missing values in text column
- Merge query tweets and response tweets using tweet id (Data with up to 20 lines of dialog)
- For general tech support chat model, only tweets to and from tech-related companies were kept ("hulu_support", "sprintcare", "comcastcares", "XboxSupport", "VerizonSupport", "TMobileHelp", "SpotifyCares", "MicrosoftHelps", "HPSupport", "DellCares", "Ask_Spectrum", "AskPlayStation", "AppleSupport", "AdobeCare")
- Removed irrelevant text from data
  - Removed @ tags at beginning of all text
  - Removed emojis
  - Removed names of customer support staff at the end of some tweets
Removed responses which ask the customer to send a DM as they do not provide useful help for customers

### Fine-tuning GODEL model
Built pipeline for model training by referencing documentation on Hugging Face transformers and GODEL. 
Basic outline:
1. Load model and tokenizer of pretrained model: "microsoft/GODEL-v1_1-large-seq2seq".
2. Obtained training data points using random sampling (99% of dataset). Remaining data was split into validation and test datasets (Had to limit the size of validation and test datasets due to memory constraints).
3. Preprocessing of text using the tokenizer and mapping function to generate model inputs.
4. Trained the model using Trainer class.

Using the same pipeline, 3 models were trained and tested: 
- Tweets to and from all tech-related companies identified earlier
- Tweets to and from AppleSupport
- Tweets to and from SpotifyCares

#### Evaluation
Used ROUGE-L to evaluate the performance of the models. ROUGE-L scores the outputs of the chat model based on the length of the longest common subsequence present in the generated output and the reference response. 
| Model      | ROUGE-L |
| ----------- | ----------- |
| General      | 0.594       |
| AppleSupport   | 0.658        |
| SpotifyCares   | 0.725        |

**Sample outputs:**\
**A.**\
User input: the camera on my iPhone does not work\
GODEL: We want to help you with your camera. What exactly is not working with your camera?\
User input: I cannot open the camera app\
GODEL: What happens when you try to open the camera app? Are you getting any error messages?\
User input: my phone returns to the home screen whenever I click on the camera app\
GODEL: Thanks for reaching out. Let's work together to get this resolved. Which iOS version are you using? You can find this in Settings > General > About.\
User input: I am using iOS 11.1.1\
GODEL: Let's check out this page: https://t.co

**B.**\
User input: I still get ads in between songs even though I subscribed to Spotify premium last month\
GODEL: Hey Matt! Does logging out, restarting your device, and logging back in help? Keep us posted\
User input: I have tried restarting and logging in again but am still getting ads\
GODEL: Sorry, John! Our team is actively investigating this behavior and we appreciate your patience while we investigate!

**C.**\
User input: is there an internet outage, I have not been able to connect to the internet\
GODEL: Good evening, I'd be happy to look into any internet issues you're having. Can you please send me your name and address, ad... https://t.co

**D.**\
User input: I cannot connect my laptop to the internet\
GODEL: Sorry to hear that. Which operating system are you using? What error message or error code do you see?\
User input: I am using windows 10 and am unable to connect to the wifi network\
GODEL: Hi. Let's sort this out. Were there any changes made to your device prior to this issue?\
User input: I did not make any changes\
GODEL: Hi there, we're looping in an expert who can help you out here. They will reply as soon as they're available.

**E.**\
User input: my PS4 is not working\
GODEL: Sorry to hear that! Please provide us more details of the issue that you are having.\
User input: I cannot switch my PS4 on\
GODEL: Sorry to know that. Follow the steps in the next link to reset the router: https://t.co

**F.**\
User input: my 4G connection is so slow\
GODEL: We can help! What speeds are you getting? Please let us know more details.\
User input: I am getting 1mbps on my phone\
GODEL: What state are you located? Do you have a Verizon Wireless account?\
User input: I am located in California and do have a Verizon wireless account\
GODEL: If you are located in California, you do not have to have a Verizon Wireless account to use our services.

**Key Findings**
- Found the specific model to be more effective at providing relevant responses. The general model can get confused about the context (e.g. the product, service or company), especially when the query is vague. This is evident in the higher ROUGE-L scores.
- Chatbot is able to provide specific and helpful responses, showing the strong ability of the model to adapt to a new context.
- Chatbot gets confused about the context sometimes (see D. & F. of sample outputs)
- Responses can be improved to provide more useful help with a larger set of training data with more helpful responses that provide specific steps for users to troubleshoot.
- Quality and quantity of training data needs to be improved significantly to achieve good responses with the chat model.

## Flask App
Created a web app using Flask for a demonstration of the fine-tuned chat models.\

![image](https://github.com/wwaihoe/GODEL-twcs/assets/91514179/b6dfe720-37ba-4907-be67-4c37fdf1dd89)

UI was created with BootStrap.\
Local database to store chat logs was implemented using SQLite.


