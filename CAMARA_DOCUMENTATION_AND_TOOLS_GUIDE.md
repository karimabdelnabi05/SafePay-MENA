# CAMARA APIs, Telecom Tools & Documentation Reference Guide

This document contains all direct links, official GitHub repositories, OpenAPI specifications, and documentation for the tools and APIs used in **SafePay MENA**.

---

## 1. Official CAMARA Project (Linux Foundation & GSMA)

CAMARA is the open-source project that defines the universal REST API specifications for all global telecom operators.

- 🌐 **Official Website:** [https://camaraproject.org/](https://camaraproject.org/)  
- 📂 **Official GitHub Organization:** [https://github.com/camaraproject](https://github.com/camaraproject)  
- 📖 **CAMARA API Commonalities & Guidelines:** [https://github.com/camaraproject/Commonalities](https://github.com/camaraproject/Commonalities)  

---

## 2. The 4 CAMARA APIs Used in SafePay MENA

Click into each repository below to read the exact OpenAPI specs (YAML/JSON), data models, and sequence diagrams:

### 1. SIM Swap API (2-Legged Server-to-Server)
- 📂 **GitHub Repository:** [https://github.com/camaraproject/SimSwap](https://github.com/camaraproject/SimSwap)  
- 📄 **What to Read:** Look at `code/API_definitions/sim_swap.yaml` to see the exact request and response payloads (`check`, `retrieve-date`).

### 2. Number Verification API (3-Legged OAuth / Mobile Data Bearer)
- 📂 **GitHub Repository:** [https://github.com/camaraproject/NumberVerification](https://github.com/camaraproject/NumberVerification)  
- 📄 **What to Read:** Check `documentation/CAMARA-API-access-and-user-consent.md` to understand how the 3-legged cellular data handshake works.

### 3. Device Status API (Roaming & Reachability)
- 📂 **GitHub Repository:** [https://github.com/camaraproject/DeviceStatus](https://github.com/camaraproject/DeviceStatus)  
- 📄 **What to Read:** Check `code/API_definitions/device_status_roaming.yaml` to see how international roaming and country codes are returned.

### 4. Device Swap API (IMEI Hardware Change)
- 📂 **GitHub Repository:** [https://github.com/camaraproject/DeviceSwap](https://github.com/camaraproject/DeviceSwap)  
- 📄 **What to Read:** Look at `code/API_definitions/device_swap.yaml` to see how hardware handset changes are flagged.

---

## 3. Developer Portals & SDKs

### Nokia Network as Code (NaC)
Nokia provides the developer platform and sandbox for querying CAMARA APIs.
- 🌐 **Developer Portal:** [https://developer.networkascode.nokia.io/](https://developer.networkascode.nokia.io/)  
- 🐍 **Python SDK Documentation:** [https://github.com/nokia/network-as-code-python](https://github.com/nokia/network-as-code-python)  

### GSMA Open Gateway
The global telecom industry alliance backing CAMARA.
- 🌐 **GSMA Open Gateway Hub:** [https://www.gsma.com/solutions-and-impact/technologies/open-gateway/](https://www.gsma.com/solutions-and-impact/technologies/open-gateway/)  

### Google AI Studio (Gemini 2.0 Flash)
The AI reasoning model that orchestrates tool calling and risk traces.
- 🌐 **Google AI Studio:** [https://aistudio.google.com/](https://aistudio.google.com/)  
- 📖 **Gemini Function Calling Docs:** [https://ai.google.dev/gemini-api/docs/function-calling](https://ai.google.dev/gemini-api/docs/function-calling)  

---

## 4. Local Hackathon Reference Guides

The official hackathon guides are also stored locally in your workspace:
- 📄 **[GSMA MENA Resource Guide](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/GSMA%20MENA%20Resource%20Guidea254feb.pdf)** - Official tool recommendations & judging tips.
- 📄 **[GSMA Mentorship Guide](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/GSMA%20MENA%20Ignite%20Hackathon%20-%20Mentorship%20Guide%20(1).pdf)** - Rules for your meeting with Eng. Abdullah (stc).
