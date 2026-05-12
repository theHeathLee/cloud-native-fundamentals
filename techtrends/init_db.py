import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

sample_posts = [
    (
        'The Rise of WebAssembly in Cloud Native Environments',
        'WebAssembly is no longer just a browser technology. Projects like Wasmtime and WASI are '
        'bringing portable, sandboxed execution to the server side, making it an interesting '
        'alternative to containers for certain workloads.'
    ),
    (
        'Understanding eBPF and Its Impact on Kubernetes Networking',
        'Extended Berkeley Packet Filter (eBPF) has transformed how we think about observability '
        'and networking in Linux. Tools like Cilium and Pixie leverage eBPF to provide deep '
        'kernel-level visibility without modifying application code.'
    ),
    (
        'GitOps: Why Declarative Infrastructure Matters',
        'The GitOps pattern treats your Git repository as the single source of truth for '
        'infrastructure state. When combined with tools like ArgoCD or Flux, teams see faster '
        'deployments and easier rollbacks compared to imperative pipelines.'
    ),
    (
        'CNCF Landscape 2024: Navigating 1000+ Projects',
        'The Cloud Native Computing Foundation now tracks over a thousand projects. This post '
        'breaks down which layers of the stack actually matter for a small team and which ones '
        'you can safely ignore until you hit serious scale.'
    ),
    (
        'Kubernetes 1.29 Highlights: What Actually Changed',
        'Release 1.29 brings several features out of alpha including improvements to sidecar '
        'containers and dynamic resource allocation. Here is a practical look at what teams '
        'should consider adopting and what is still too early.'
    ),
    (
        'Choosing a Service Mesh in 2024: Istio vs Linkerd vs Cilium',
        'Service meshes have matured significantly. Istio has simplified its architecture by '
        'removing the need for a separate sidecar in ambient mode. Linkerd remains the lightest '
        'option. Cilium offers a kernel-based approach that sidesteps proxies entirely.'
    ),
    (
        'Platform Engineering vs DevOps: What Is the Difference?',
        'Platform engineering is the practice of building internal developer platforms that '
        'reduce cognitive load. While DevOps focuses on culture and collaboration, platform '
        'engineering focuses on building reusable, self-service infrastructure tooling.'
    ),
]

cur.executemany('INSERT INTO posts (title, content) VALUES (?, ?)', sample_posts)
conn.commit()
conn.close()
