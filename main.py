from fasthtml.common import *

# Create minimal FastHTML app
app, rt = fast_app()


@rt("/")
def get():
    """Main page with client-side key generation"""
    js_code = """
    document.getElementById('generate-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        try {
            // Generate Ed25519 key pair using WebCrypto
            const keyBuffer = new Uint8Array(32);
            window.crypto.getRandomValues(keyBuffer);
            
            // Convert to hex
            const privateKeyHex = Array.from(keyBuffer)
                .map(b => b.toString(16).padStart(2, '0'))
                .join('');
                
            const keyDisplay = document.querySelector('.key-display');
            keyDisplay.textContent = privateKeyHex;
            document.querySelector('#copy-btn').onclick = (e) => copyToClipboard(e, privateKeyHex);
        } catch (e) {
            const keyDisplay = document.querySelector('.key-display');
            keyDisplay.textContent = 'Error generating key';
            keyDisplay.classList.add('text-danger');
            console.error(e);
        }
    });

    async function copyToClipboard(e, text) {
        try {
            await window.navigator.clipboard.writeText(text);
            const btn = e.currentTarget;
            btn.innerHTML = '<i class="bi bi-check2"></i>';
            setTimeout(() => {
                btn.innerHTML = '<i class="bi bi-clipboard"></i>';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
        }
    }
    """

    styles = """
    .key-display {
        font-size: 0.875rem;
        word-break: break-all;
        background: var(--bs-light);
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 0;
        border: 1px solid var(--bs-border-color);
    }
    """

    content = Container(
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"),
        Style(styles),
        Div(
            H1("Private Key Generator", cls="text-center mb-4"),
            Div(
                H5("About this tool:", cls="mb-3"),
                Ul(
                    Li("Generates Ed25519 private keys"),
                    Li("All computation happens in your browser - no data is sent to any server"),
                    Li(
                        "Full source code available on ",
                        A("Replit", href="https://replit.com/t/fewsats/repls/pk-generator/view"),
                        " - feel free to inspect and run it yourself"
                    ),
                    cls="text-muted"
                ),
                Div(
                    "Terminal equivalent:",
                    Code("openssl genpkey -algorithm ed25519 -outform der | xxd -p -c 32", 
                         cls="ms-2 p-2 bg-light"),
                    cls="mt-3 text-muted small"
                ),
                cls="alert alert-info"
            ),
            Form(
                Button("Generate New Key",
                      type="submit",
                      cls="btn btn-primary d-block mx-auto"),
                cls="mt-4",
                id="generate-form"
            ),
            Card(
                Div(H5("Private Key (Hex)", cls="card-title mb-0"),
                    cls="card-header bg-light"),
                Div(
                    Div(
                        Code("Click 'Generate New Key' to create a key", 
                             cls="key-display flex-grow-1"),
                        Button(I(cls="bi bi-clipboard"), 
                              cls="btn btn-outline-secondary ms-2",
                              id="copy-btn"),
                        cls="d-flex align-items-center"
                    ),
                    cls="card-body"
                ),
                cls="mt-4"
            ),
            Script(js_code),
            cls="container py-5"
        )
    )
    return Title("Ed25519 Key Generator"), content


# Start server
if __name__ == "__main__":
    serve()

