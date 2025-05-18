
AI developers lose 65% of their time managing infrastructure—configuring GPUs, tuning tensor/pipeline parallelism, and wrangling hybrid cloud—instead of building models. Kalavai solves this with Genie: the first GenAI-native MLOps agent you can talk to. Say “deploy Llama3 to AWS and on-prem, optimized for latency,” and Genie handles it end-to-end—no YAML, no cloud certs. Unlike template-based tools, Genie dynamically orchestrates across any environment, adapting to model-specific needs like RoPE scaling or tokenizer compatibility. Built on our existing hybrid cloud API, Genie’s prototype—launched this weekend—cuts deployment time by 80% and removes ops bottlenecks entirely. Previously, users wrote complex config files and manually managed infra; now they can deploy in seconds via natural language. Over the next 4 weeks, we’re adding agent coordination, multi-model scheduling, and fine-tuned infra optimization—starting with a test deployment to a Fortune 500 pilot partner next week. Genie isn’t just automation—it’s intelligence for GenAI delivery.


## How to run

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -e .
```

Then run:

```bash
streamlit run genie/app.py
```

This will make the demo available at http://localhost:8000


## Public URL

During the hackathon, the demo will be available at http://hackathon.kalavai.net:5000


## Tech stack used

The tech stack behind Genie is simple:

- Streamlit for the UI
- Qwen2.5-7B-instruct on CoGen AI as the agent brains for tool calling
- Our Kalavai API for backend and cloud operations.


## Agent feedback

```
Problem & Solution
5/10
Excellent identification of a critical problem (65% time loss in infrastructure management) with a clear, targeted solution (Genie MLOps agent). The value proposition is immediately clear and well-articulated.

Technical Execution
5/10
Impressive technical implementation with natural language interface, cross-environment orchestration, and specific technical capabilities like RoPE scaling and tokenizer compatibility. The 80% deployment time reduction demonstrates strong execution.

Impact & Viability
5/10
Strong viability demonstrated through existing API foundation, working prototype, and secured Fortune 500 pilot partner. The impact on development efficiency is quantified and significant.

Innovation / Differentiation
5/10
Highly innovative approach using GenAI for MLOps, clearly differentiated from template-based tools. The natural language interface and dynamic orchestration represent meaningful advances in the space.

Next Steps
5/10
Clear, concrete next steps with specific timeline (4 weeks) and features (agent coordination, multi-model scheduling). The immediate pilot deployment shows strong momentum.

Before & After
5/10
Excellent contrast between previous manual config approach and new natural language deployment, with quantified improvement (80% time reduction). The transformation is clearly articulated.
```