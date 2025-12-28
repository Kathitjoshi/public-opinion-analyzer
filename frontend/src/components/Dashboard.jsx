function Dashboard({ data }) {
  if (!data || Object.keys(data).length === 0) {
    return <p>Thx for your time!!</p>;
  }

  return (
    <table border="1" cellPadding="8">
      <thead>
        <tr>
          <th>Sentiment</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(data).map(([sentiment, count]) => (
          <tr key={sentiment}>
            <td>{sentiment}</td>
            <td>{count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Dashboard;
