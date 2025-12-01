# MSA_8770_Project_Madoff
MSA_8770 Project

To Run this project, just run each cell sequentially and install the libraries in requirements.txt as:
    pip install -r requirements.txt


# Tri-Agent Financial Analyst Prototype

This repository contains three Jupyter notebooks that together form a simple multi-agent financial-analysis system:

- **Agent_Buffett.ipynb** – Scrapes SEC data, builds financial tables, and provides a financial-metrics tool.
- **Agent_Dalio.ipynb** – (Future) Scrapes news and produces sentiment lookups.
- **Agent_Graham.ipynb** – Runs the Q&A system and orchestrates the agents.

All logic is contained in these notebooks. No additional scripts are required.

---

## 1. Overview for New Users

The workflow is:

1. **Scrape financial fundamentals** using Agent_Buffett.  
2. **(Optional)** Scrape news/sentiment using Agent_Dalio.  
3. **Run the Tri-Agent Q&A** using Agent_Graham.  
4. **Validate answers** using the scoring rubric in your paper.

Each notebook is designed to run independently in Jupyter / VS Code / or Google Colab.

---

## 2. How to Scrape the Data (Fundamentals)

Open **Agent_Buffett.ipynb**.

1. Set your SEC email identity:  
   ```python
   set_identity("youremail@example.com")
Choose your tickers by editing the list:

python
Copy code
companies = ["MSFT", "AAPL", "NVDA", "GME", "V"]
This is where you select your own stocks.

Run the scraping cell:

python
Copy code
results, summary = scrape_companies(companies, years=5)
Upload the scraped financial tables to Qdrant by running the “Save to Qdrant Cloud” cell.

Run the cell that defines the financial metrics tool
(tool_fetch_financial_metrics) that the Q&A agent will use later.

This completes all fundamental data ingestion.

3. How to Select Your Own Stocks
To analyze different stocks:

Edit the ticker list inside Agent_Buffett.ipynb.

Re-run:

the scraping block

the “push to Qdrant” block

(If Dalio is used) edit the same ticker list inside Agent_Dalio.ipynb.

The system will then be able to answer Q&A for your chosen tickers.

4. Where to Run the Q&A
Open Agent_Graham.ipynb.

Run all setup cells (imports, tool loading, agent graph creation).

Locate the helper function:

python
Copy code
Agent_Graham("Your question here")
Ask free-form questions, for example:

python
Copy code
Agent_Graham("Should I sell GameStop?")
Agent_Graham("Compare Microsoft and Apple earnings.")
To evaluate the system using your nine predefined questions, run the final evaluation cell in the notebook.

Graham will automatically call Buffett (and Dalio, when implemented) to gather evidence.

5. How to Validate the Results
Use three scoring dimensions:

Accuracy (0–1)
Does the final recommendation make sense and match the baseline truth?

Truthfulness (0–1)
Are the statements supported by:

the financial metrics scraped by Buffett

and/or the news returned by Dalio?

Deduct points when the agent invents unsupported facts.

Excessive Tools Called (count)
Count cases where:

Graham re-prompts a sub-agent more than 3 times

Buffett or Dalio repeat tool calls with the same ticker after failures

The system loops unnecessarily

You can store results in a simple scoring table (as in your paper).

6. Best Practices for Using the System
Always re-scrape after changing tickers.

Check the Qdrant collection names if results don’t load.

Run notebooks top-to-bottom without skipping cells.

Monitor tool-call behavior — repeated failures usually indicate missing data.

When adding new features, keep one-way agent hierarchy (Graham → Buffett/Dalio) to avoid feedback loops.

7. Files in This Repo
File	Purpose
Agent_Buffett.ipynb	Scrapes fundamentals + financial metrics tool
Agent_Dalio.ipynb	Scrapes news + sentiment tool (future)
Agent_Graham.ipynb	Full Q&A tri-agent orchestration

8. Quick Start
Open Agent_Buffett.ipynb, set tickers, run scrape, push to Qdrant.

(Optional) Open Agent_Dalio.ipynb, scrape news and push to Qdrant.

Open Agent_Graham.ipynb, run the graph, then ask questions using Agent_Graham().

Score the responses using the evaluation rubric.
