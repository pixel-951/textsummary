#!/usr/bin/env python

from transformers import pipeline



class Summarizer: 

    def __init__(self, model:str="facebook/bart-large-cnn", max_length:int=130): 
        self.summarizer = pipeline("summarization", model=model) # more so model selection vs downloading of weights again, needs input validation
        self.max_length = max_length

    

    def summarize_text(self, text:str) -> str: 
        
        result = self.summarizer(text, max_length=self.max_length, min_length=30)
        summary = result[0]['summary_text']
        return summary

