```bash
# Run the demo:
python3 px-demo.py
```
```bash
# Associate a creative template with the rewrite macros:
export ADZERK_API_KEY=${your_kevel_network_api_key}
python3 upsert-creative-template-rewrite.py ${network_id} ${creative_template_id}
```
```bash
# Disassociate a creative template with the rewrite macros:
export ADZERK_API_KEY=${your_kevel_network_api_key}
python3 delete-creative-template-rewrite.py ${network_id} ${creative_template_id}
```
```bash
# Get the rewrite macros associated with a creative template:
export ADZERK_API_KEY=${your_kevel_network_api_key}
python3 get-creative-template-rewrite.py ${network_id} ${creative_template_id}
```
