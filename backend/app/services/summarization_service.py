from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
from fastapi import HTTPException
from app.core.config import settings
from typing import List, Dict, Any
import json
import os
import torch

class SummarizationService:
    _summarizer = None
    _text_generator = None
    _tokenizer = None

    @staticmethod
    def _load_models():
        """Load or initialize the models"""
        if SummarizationService._summarizer is None:
            try:
                # Create cache directory if it doesn't exist
                os.makedirs(settings.HUGGINGFACE_CACHE_DIR, exist_ok=True)
                
                # Load summarization model and tokenizer (using a smaller model)
                model_name = "facebook/bart-large-cnn"
                SummarizationService._tokenizer = AutoTokenizer.from_pretrained(
                    model_name,
                    cache_dir=settings.HUGGINGFACE_CACHE_DIR
                )
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    model_name,
                    cache_dir=settings.HUGGINGFACE_CACHE_DIR
                )
                
                # Create summarization pipeline
                SummarizationService._summarizer = pipeline(
                    "summarization",
                    model=model,
                    tokenizer=SummarizationService._tokenizer,
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Load text generation model (using a larger model for better extraction)
                # Use flan-t5-large or flan-t5-xl for better results if GPU memory allows
                generation_model = "google/flan-t5-large"
                SummarizationService._text_generator = pipeline(
                    "text2text-generation",
                    model=generation_model,
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error loading models: {str(e)}"
                )

    @staticmethod
    def summarize_text(text: str, max_length: int = None, min_length: int = 30):
        """
        Summarize text using Hugging Face's BART model
        """
        try:
            # Load model if not already loaded
            SummarizationService._load_models()
            
            # Calculate appropriate max_length if not provided
            if max_length is None:
                # Tokenize the input text
                tokens = SummarizationService._tokenizer.encode(text)
                # Set max_length to 50% of input length, but not less than min_length
                max_length = max(min_length, len(tokens) // 2)
            
            # Split text into chunks if it's too long
            max_chunk_length = 1024
            chunks = []
            current_chunk = []
            current_length = 0
            
            for sentence in text.split('.'):
                sentence = sentence.strip() + '.'
                sentence_length = len(SummarizationService._tokenizer.encode(sentence))
                
                if current_length + sentence_length > max_chunk_length:
                    if current_chunk:
                        chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = sentence_length
                else:
                    current_chunk.append(sentence)
                    current_length += sentence_length
            
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            # Summarize each chunk
            summaries = []
            for chunk in chunks:
                summary = SummarizationService._summarizer(
                    chunk,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )[0]['summary_text']
                summaries.append(summary)
            
            # Combine summaries
            final_summary = ' '.join(summaries)
            
            # If the final summary is too long, summarize it again
            if len(SummarizationService._tokenizer.encode(final_summary)) > max_chunk_length:
                final_summary = SummarizationService._summarizer(
                    final_summary,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                    truncation=True
                )[0]['summary_text']
            
            return final_summary
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")
    
    @staticmethod
    def extract_action_items(text: str) -> List[Dict[str, Any]]:
        """
        Extract action items and owners from meeting transcript
        """
        try:
            # Load model if not already loaded
            SummarizationService._load_models()
            
            # Create prompt for action items
            prompt = f"""Extract action items from this meeting transcript. For each action item, identify:
            1. Task title (be specific)
            2. Description (include context and requirements)
            3. Assignee (who is responsible)
            4. Due date (if mentioned)
            
            Format the response as a JSON array of objects with these fields.
            If there are no explicit action items, analyze the discussion to identify implied tasks, next steps, 
            or follow-up items that participants should complete. Look for questions that need answers, 
            information that needs to be gathered, or issues that need to be resolved.
            
            Example output format:
            [
              {{
                "title": "Research potential solutions",
                "description": "Investigate available options for the problem discussed",
                "assignee": "John",
                "due_date": "Next week"
              }}
            ]
            
            Meeting transcript:
            {text}
            
            Return the response as a valid JSON array. If there are absolutely no action items or implied tasks,
            return an empty array: []"""
            
            # Generate response
            response = SummarizationService._text_generator(
                prompt,
                max_length=1024,
                num_return_sequences=1,
                temperature=0.7
            )[0]['generated_text']
            
            try:
                # Try to parse the response as JSON
                # Extract JSON part of the response if needed
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_text = response[json_start:json_end]
                    action_items = json.loads(json_text)
                else:
                    action_items = json.loads(response)
                    
                if not isinstance(action_items, list):
                    action_items = [action_items]
                return action_items
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract items from text
                items = []
                lines = response.split('\n')
                current_item = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('title:'):
                        if current_item and 'title' in current_item:
                            items.append(current_item)
                        current_item = {'title': line[6:].strip()}
                    elif line.startswith('description:'):
                        current_item['description'] = line[12:].strip()
                    elif line.startswith('assignee:'):
                        current_item['assignee'] = line[9:].strip()
                    elif line.startswith('due_date:'):
                        current_item['due_date'] = line[9:].strip()
                
                if current_item and 'title' in current_item:
                    items.append(current_item)
                
                return items
                
        except Exception as e:
            print(f"Error extracting action items: {str(e)}")
            return []
    
    @staticmethod
    def extract_decisions(text: str) -> List[Dict[str, Any]]:
        """
        Extract decisions and their rationale from meeting transcript
        """
        try:
            # Load model if not already loaded
            SummarizationService._load_models()
            
            # Create prompt for decisions
            prompt = f"""Extract decisions made during this meeting. For each decision, identify:
            1. Decision title (what was decided)
            2. Description (context and details of the decision)
            3. Decision maker (who made or approved the decision)
            4. Rationale (why this decision was made)
            
            Format the response as a JSON array of objects with these fields.
            If there are no explicit decisions, analyze the discussion to identify implied agreements, 
            consensus points, or conclusions reached by participants.
            
            Example output format:
            [
              {{
                "title": "Proceed with option A",
                "description": "The team agreed to move forward with implementing option A",
                "decision_maker": "Team lead",
                "rationale": "Option A provides the best balance of cost and features"
              }}
            ]
            
            Meeting transcript:
            {text}
            
            Return the response as a valid JSON array. If there are absolutely no decisions or implied agreements,
            return an empty array: []"""
            
            # Generate response
            response = SummarizationService._text_generator(
                prompt,
                max_length=1024,
                num_return_sequences=1,
                temperature=0.7
            )[0]['generated_text']
            
            try:
                # Try to parse the response as JSON
                # Extract JSON part of the response if needed
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_text = response[json_start:json_end]
                    decisions = json.loads(json_text)
                else:
                    decisions = json.loads(response)
                    
                if not isinstance(decisions, list):
                    decisions = [decisions]
                return decisions
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract items from text
                items = []
                lines = response.split('\n')
                current_item = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('title:'):
                        if current_item and 'title' in current_item:
                            items.append(current_item)
                        current_item = {'title': line[6:].strip()}
                    elif line.startswith('description:'):
                        current_item['description'] = line[12:].strip()
                    elif line.startswith('decision_maker:'):
                        current_item['decision_maker'] = line[15:].strip()
                    elif line.startswith('rationale:'):
                        current_item['rationale'] = line[10:].strip()
                
                if current_item and 'title' in current_item:
                    items.append(current_item)
                
                return items
                
        except Exception as e:
            print(f"Error extracting decisions: {str(e)}")
            return [] 