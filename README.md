# opa-gatekeeper-concurrency-issue
Proof-of-Concept of a concurrency issue in OPA/Gatekeeper using data replication.

OPA/Gatekeeper [data replication](https://open-policy-agent.github.io/gatekeeper/website/docs/sync/) mechanism allows policies to access the Kubernetes cluster state. 
During data replication, OPA/Gatekeeper does not wait for the replication to finish before processing a request, potentially leading to inconsistencies between the resources replicated in OPA/Gatekeeper and the resources actually present in the cluster. Such inconsistency eventually leads to policy bypass, as demonstrated in this PoC.

## How to reproduce
In the reproductible example, we are enforcing "Unique Service Selector" policy (from https://docs.rafay.co/recipes/governance/service_selector_policy/) so two different Services cannot be created with the same app selector.  Service 1 and Service 2 have the same app selector `service`. However, by running multiple concurrent request, the policy is eventually bypassed and the two services are created with the same selector. Note that this violation should normally appears during audit afterwards.


The following video shows the PoC running in a Kubernetes cluster using Ubuntu 18.04.5, kubectl v1.20, gatekeeper v3.1.3.

<img src="poc.gif" width="600" />

Steps:
Using a Kubernetes cluster:
- Deploy OPA/Gatekeeper: `kubectl apply -f gatekeeper.yaml`. The OPA/Gatekeeper pods are deployed in the `gatekeeper-system` namespace.
- Enable the data replication mechanism on Services: `kubectl apply -f config.yaml`.
- Enforce the policy: `kubectl apply -f template.yaml; kubectl apply -f constraint.yaml`. 
- Run the PoC: `python3 script.py`. After a few tries, Service 1 and Service 2 should eventually be created and coexist in the cluster, result of the policy bypass.

More specifically, the script tries to create the two concurrent services almost at the same time (Popen doesn't wait for the process to finish), and monitor the creation success or failure.
