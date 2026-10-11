import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [formMessage, setFormMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const [form, setForm] = useState({
    name: "",
    price: "",
    stock: "0",
  });

  async function loadProducts() {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/products`);

      if (!response.ok) {
        throw new Error("Failed to load products.");
      }

      const data = await response.json();
      setProducts(data);
    } catch {
      setError("Could not connect to the API. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProducts();
  }, []);

  function handleInputChange(event) {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));

    setFormMessage("");
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setFormMessage("");
    setSubmitting(true);

    try {
      const response = await fetch(`${API_URL}/products`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: form.name.trim(),
          price: Number(form.price),
          stock: Number(form.stock),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        const detail = Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(" ")
          : data.detail;

        throw new Error(detail || "Could not create product.");
      }

      setFormMessage(`Success! "${data.name}" was added to your catalog.`);
      setForm({ name: "", price: "", stock: "0" });

      await loadProducts();
    } catch (submissionError) {
      setFormMessage(
        submissionError.message === "Failed to fetch"
          ? "Could not connect to the API. Check that the backend is running."
          : submissionError.message
      );
    } finally {
      setSubmitting(false);
    }
  }

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(search.toLowerCase())
  );

  const inStockCount = products.filter((product) => product.stock > 0).length;
  const outOfStockCount = products.filter((product) => product.stock === 0).length;

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <span className="brand-icon">Q</span>
          <span>
            QA<span className="brand-accent">Store</span>
          </span>
        </div>

        <span className="api-status">
          <span className={`status-dot ${error ? "status-error" : ""}`} />
          {loading ? "Connecting..." : error ? "API unavailable" : "API connected"}
        </span>
      </header>

      <section className="content">
        <div className="page-heading">
          <div>
            <p className="eyebrow">INVENTORY MANAGEMENT</p>
            <h1>Products</h1>
            <p className="subtitle">
              Manage your catalog and monitor stock levels.
            </p>
          </div>

          <span className="product-count">
            {loading ? "Loading..." : `${filteredProducts.length} products`}
          </span>
        </div>

        <section className="stats">
          <article className="stat-card">
            <p>Total products</p>
            <strong>{loading ? "—" : products.length}</strong>
            <span>In your catalog</span>
          </article>

          <article className="stat-card">
            <p>In stock</p>
            <strong>{loading ? "—" : inStockCount}</strong>
            <span>Available products</span>
          </article>

          <article className="stat-card">
            <p>Out of stock</p>
            <strong>{loading ? "—" : outOfStockCount}</strong>
            <span>Need attention</span>
          </article>
        </section>

        <section className="table-card">
          <div className="table-heading">
            <div>
              <h2>Product catalog</h2>
              <p>Browse and search your inventory.</p>
            </div>

            <input
              aria-label="Search products"
              placeholder="Search products..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              disabled={loading || Boolean(error)}
            />
          </div>

          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Product ID</th>
                  <th>Price</th>
                  <th>Stock</th>
                  <th>Status</th>
                </tr>
              </thead>

              <tbody>
                {loading && (
                  <tr>
                    <td colSpan="5" className="empty-state">
                      Loading products...
                    </td>
                  </tr>
                )}

                {!loading && error && (
                  <tr>
                    <td colSpan="5" className="empty-state">
                      {error}
                    </td>
                  </tr>
                )}

                {!loading && !error && filteredProducts.map((product) => (
                  <tr key={product.id}>
                    <td className="product-name">{product.name}</td>
                    <td>PRD-{String(product.id).padStart(3, "0")}</td>
                    <td>{Number(product.price).toFixed(2)} RON</td>
                    <td>{product.stock}</td>
                    <td>
                      <span
                        className={`stock-badge ${
                          product.stock > 0 ? "available" : "unavailable"
                        }`}
                      >
                        {product.stock > 0 ? "In stock" : "Out of stock"}
                      </span>
                    </td>
                  </tr>
                ))}

                {!loading && !error && filteredProducts.length === 0 && (
                  <tr>
                    <td colSpan="5" className="empty-state">
                      No products found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <footer className="table-footer">
            {loading
              ? "Fetching data from API..."
              : error
                ? "Unable to retrieve inventory."
                : `Showing ${filteredProducts.length} of ${products.length} products`}
          </footer>
        </section>

        <section className="table-card add-product-card">
          <div className="form-heading">
            <div>
              <h2>Add a product</h2>
              <p>Create a product and save it to the database.</p>
            </div>
          </div>

          <form className="product-form" onSubmit={handleSubmit}>
            <label>
              Product name
              <input
                name="name"
                type="text"
                placeholder="e.g. Wireless Headphones"
                value={form.name}
                onChange={handleInputChange}
                minLength={1}
                maxLength={100}
                required
              />
            </label>

            <label>
              Price (RON)
              <input
                name="price"
                type="number"
                placeholder="199.99"
                value={form.price}
                onChange={handleInputChange}
                min="0.01"
                step="0.01"
                required
              />
            </label>

            <label>
              Stock quantity
              <input
                name="stock"
                type="number"
                value={form.stock}
                onChange={handleInputChange}
                min="0"
                step="1"
                required
              />
            </label>

            <button type="submit" disabled={submitting}>
              {submitting ? "Adding product..." : "Add product"}
            </button>
          </form>

          {formMessage && (
            <p
              className={`form-message ${
                formMessage.startsWith("Success!")
                  ? "form-success"
                  : "form-error"
              }`}
              role="status"
              aria-live="polite"
            >
              {formMessage}
            </p>
          )}
        </section>

        <p className="footer-note">
          QA Automation Project · React · FastAPI · SQLite · Automated Testing
        </p>
      </section>
    </main>
  );
}

export default App;