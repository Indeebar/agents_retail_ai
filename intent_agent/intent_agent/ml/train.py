import torch
from torch.utils.data import DataLoader
from transformers import DistilBertForSequenceClassification
from transformers import AdamW

from intent_dataset import IntentDataset

def train():
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    #Load Dataset
    dataset = IntentDataset("../data/intent_dataset.csv")


    dataloader=DataLoader(dataset,batch_size=4,shuffle=True)
    
    num_labels=len(set(dataset.labels)) #no of labels=no of unique intents

    #Load Model
    model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=num_labels
    )

    
    model.to(device)
    model.train()

    #optimizer
    optimizer=AdamW(model.parameters(),lr=5e-5)

    print("Training model...")

    for batch_idx,batch in enumerate(dataloader):
        optimizer.zero_grad()


        input_ids=batch["input_ids"].to(device)
        attention_mask=batch["attention_mask"].to(device)
        labels=batch["labels"].to(device)

        outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask,
        labels=labels
        )


        loss=outputs.loss   
        loss.backward()
        optimizer.step()

        print(f"Batch {batch_idx+1}/{len(dataloader)} Loss: {loss.item()}")

    print("Training complete.")

    # Save model
    save_path = "../models/intent_classifier"
    model.save_pretrained(save_path)
    dataset.tokenizer.tokenizer.save_pretrained(save_path)

    print(f"Model saved to {save_path}")
    

if __name__=="__main__":     
    train()


    


