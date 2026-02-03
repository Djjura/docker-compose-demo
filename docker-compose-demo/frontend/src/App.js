import { useEffect, useState } from "react";

function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/users")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Backend error");
        }
        return res.json();
      })
      .then((data) => {
        console.log("USERS FROM API:", data); 
        setUsers(data); // ✅ data je ARRAY
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading users...</p>;
  if (error) return <p>Error: {error}</p>;
  if (users.length === 0) return <p>No users found</p>;

  return (
    <div style={{ padding: "20px" }}>
      <h1>Users</h1>

      <ul>
        {users.map((u) => (
          <li key={u.id}>
            <strong>
              {u.first_name} {u.last_name}
            </strong>{" "}
            – age: {u.age}, born: {u.date_of_birth}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
