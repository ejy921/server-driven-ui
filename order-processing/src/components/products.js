import React, { useEffect, useState } from "react";

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("Fetching products")
    fetch('/api/products')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading products..</p>
  }
  if (error) {
    return <p>Error: {error}</p>
  }

  return (
    <div>
      <ul>
        {products.map((product, index) => (
          <li key={index}>
            <p><strong>Name:</strong> {product.name}</p>
            <p><strong>Price:</strong> ${product.price.toFixed(2)}</p>
            <p><strong>Quantity:</strong> {product.quantity}</p>
          </li>
        ))}
      </ul>
    </div>
  )
};

export default ProductList;