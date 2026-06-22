function ModelPerformance() {
  return (
    <div
      style={{
        background: "white",
        borderRadius: "15px",
        padding: "20px"
      }}
    >
      <h3>AI Model Performance</h3>

      <p>Sentiment Model: 92.4%</p>
      <p>Classification Model: 89.7%</p>
      <p>Priority Prediction: 91.1%</p>

      <h2
        style={{
          marginTop: "20px",
          color: "#7c3aed"
        }}
      >
        Overall Accuracy: 91.1%
      </h2>
    </div>
  );
}

export default ModelPerformance;