import mongoose from "mongoose";

const connectDb = async (MONGO_URI) => {
  const dbName = "HealthCare Database";
  await mongoose.connect(MONGO_URI);
  console.log(`connected to ${dbName}...`);
};

export default connectDb;
