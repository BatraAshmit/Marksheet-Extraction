AI Marksheet Extraction API
Overview

This project implements an AI-based API for extracting structured information from academic marksheets (images or PDFs). The API processes unstructured OCR output and returns a well-defined JSON response containing extracted fields along with confidence scores that indicate the reliability of each field.

The system is designed to be robust, layout-agnostic, and generalizable across different boards, universities, and marksheet formats.

Key Capabilities

--Supports JPG, PNG, and PDF marksheets
--Extracts structured academic data using an LLM-assisted normalization layer
--Returns field-level confidence scores (0–1)
--Handles multiple requests concurrently using FastAPI
--Provides consistent JSON schema across documents
--Includes error handling for invalid files and extraction failures
--API-key–based request authentication

Technology Stack
--Backend: Python, FastAPI
--OCR: Open-source OCR libraries
--LLM: OpenAI GPT model (used only for structuring and validation)
--Schema Validation: Pydantic
--Authentication: Header-based API key
--All non-LLM components are implemented using open-source libraries only.


API Input
--File types: JPG / PNG / PDF
--Maximum file size: 10 MB
--Authentication: API key passed via request headers

API Output
--The API returns a structured JSON object containing:

--Candidate Details
Name
Father/Mother’s Name
Roll Number
Registration Number
Date of Birth
Exam Year
Board / University
Institution

--Subject-wise Information
For each subject:
Subject name
Maximum marks / credits
Obtained marks / credits
Grade (if available)
Summary Information
Overall result / division / grade
Issue date and place (if present)

JSON Schema Design
--Fields are grouped logically (candidate details, subjects, summary).
--Each field includes both value and confidence.
--Schema remains consistent even when values are missing.
--Designed to support future extensions such as bounding boxes or batch processing.

Confidence Scoring Approach
--Confidence scores are generated during the LLM normalization stage and reflect the model’s certainty in each extracted field.

The score is influenced by:
--Clarity of OCR text
--Semantic consistency of the extracted value
--Field validation (e.g., numeric fields, dates, identifiers)
--Degree of inference required


Error Handling
The API gracefully handles:
--Unsupported file formats
--Files exceeding size limits
--Corrupted or unreadable documents
--Missing or invalid API keys
--API qouta limit exceeded
--LLM failures or quota/network issues
In failure scenarios, the API returns a valid JSON structure with low-confidence values instead of crashing.
