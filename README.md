# opa-gatekeeper-concurrency-issue
PoC of a concurrency issue in OPA/Gatekeeper using data replication

During data replication, it seems like Gatekeeper doesn't wait for the replication to finish before processing to further request, leading to cache inconsistency between the replicated resources in OPA and the resource actually presnt in the cluster. Thus, it can lead to policy bypass.

In the reproductible example, I'm enforcing an "Unique Service Selector" policy (from https://docs.rafay.co/recipes/governance/service_selector_policy/) so two services can't be created with the same Selector. However, by running multiple concurrent request, sometimes the policy is bypassed and two services are created with the same Selector (note that this violations should normally appears during audit afterwards).

example.png is the script running on my machine and leading to the flaw after 6 attempts.
slide.png is just a quick explaination of the script output.

### How to reproduce

Setup :
Ubuntu 18.04.5, kubectl v1.20, gatekeeper v3.1.3

- On a k8s cluster running with Gatekeeper, apply the template.yaml and the constraint.yaml file.
- Run the python script.py

The script tries to create the two concurrent services almost at the same time (Popen doesn't wait for the process to finish), and monitor the creation success or failure. Having success in both Service1 and Service2 creation means the enforced policy in Gatekeeper has been bypassed.
