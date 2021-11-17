# opa-gatekeeper-concurrency-issue
PoC of a concurrency issue in OPA/Gatekeeper using data replication

OPA/Gatekeeper [data replication](https://open-policy-agent.github.io/gatekeeper/website/docs/sync/) mechanism allows policies to access the Kubernetes cluster state. 
During data replication, OPA/Gatekeeper does not wait for the replication to finish before processing a request, potentially leading to inconsistencies between the replicated resources in OPA/Gatekeeper and the resources actually presnt in the cluster. Such inconsistency eventually leads to policy bypass.

## How to reproduce
In the reproductible example, we are enforcing "Unique Service Selector" policy (from https://docs.rafay.co/recipes/governance/service_selector_policy/) so two different Services cannot be created with the same app selector. However, by running multiple concurrent request, the policy is eventually bypassed and two services are created with the same selector. Note that this violations should normally appears during audit afterwards. Service 1 and Service 2 have the same app selector `service`.


The following video shows the PoC running in a Kubernetes cluster using Ubuntu 18.04.5, kubectl v1.20, gatekeeper v3.1.3.

<img src="poc.gif" width="40" height="40" />

Steps:
- Use a Kubernetes cluster.
- Deploy OPA/Gatekeeper: `kubectl apply -f gatekeeper.yaml`. The OPA/Gatekeeper pods are deployed in the `gatekeeper-system` namespace.
- Use data replication on Services: `kubectl apply -f config.yaml`.
- Enforce policy: `kubectl apply -f template.yaml; kubectl apply -f constraint.yaml`. 
- Run the PoC: `python3 script.py`.

After a few tries, Service 1 and Service 2 should eventually be created and coexist in the cluster, leading to policy bypass.

More specifically, the script tries to create the two concurrent services almost at the same time (Popen doesn't wait for the process to finish), and monitor the creation success or failure. Having success in both Service1 and Service2 creation means the enforced policy in Gatekeeper has been bypassed.
