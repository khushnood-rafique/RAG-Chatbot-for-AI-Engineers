# RAG Chatbot for AI Engineers

* This is a RAG-based AI Assistant created especially for AI engineers and researchers. It leverages its knowledge from 3 very well-known books, "AI Engineering" by Chip Huyen, "Prompt Engineering" by John Berryman and Albert Ziegler, and "Hands-On Large Language Models" by Alammar and Grootendorst. The language model used in the project was Gemma 3-12B. I used the Ollama platform to fetch the model locally. The model can be easily swapped for any other model.

* The code is very modular, so system prompts can easily be experimented with.

* The project runs using Flask on port 8080.

* Vector DB used was Pinecone. 

* AWS was used for deployment.

## Requirements:

* The pdfs used in the project have been removed due to copyright issues. You can buy your copies from here:
1) https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/
2) https://www.oreilly.com/library/view/ai-engineering/9781098166298/
3) https://www.oreilly.com/library/view/prompt-engineering-for/9781098156145/

* Or find another ways to get them ;)

* Create an account on Pinecone and get an API key for free: https://www.pinecone.io/?utm_term=pinecone%20vector%20database&utm_campaign=brand-eu&utm_source=adwords&utm_medium=ppc&hsa_acc=3111363649&hsa_cam=21023356007&hsa_grp=156209469342&hsa_ad=690982079000&hsa_src=g&hsa_tgt=kwd-1538083228315&hsa_kw=pinecone%20vector%20database&hsa_mt=e&hsa_net=adwords&hsa_ver=3&gad_source=1&gad_campaignid=21023356007&gbraid=0AAAAABrtGFAHWnQ-SIzOXafa2V0tLQOCz&gclid=Cj0KCQjw-4XFBhCBARIsAAdNOksvn8rtG8gEgiAon4QmWCKhe-CX1piPR0TgE_AxP6D98uYh7waauo4aAquXEALw_wcB

* All libraries are avaiable in "requirements.txt" file.

* System prompt in "prompt.py" file.

* Get Ollama from here: https://ollama.com/

* Usefull Ollama commands: 'ollama list', 'ollama ps', 'ollama run [model-name]', 'ollama serve'

## AWS Deployment

* EC2 access is required

* ECR to save your docker image in aws


### Steps to deployment:

1. Build docker image of the source code

2. Push docker image to ECR

3. Launch EC2 

4. Pull image from ECR to EC2

5. Lauch docker image in EC2

* Policies required:

1. AmazonEC2ContainerRegistryFullAccess

2. AmazonEC2FullAccess

### Commands for EC2 (to be run in sequence):

sudo apt-get update -y

sudo apt-get upgrade

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker

### Then confiure EC2 as self-hosted runner.