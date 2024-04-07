import express from "express";
import dotenv from "dotenv";
import connectDb from "./config/configDB.js";
import morgan from "morgan";
import userRoutes from "./routes/userRoutes.js";
// import doctorRoutes from "./routes/doctorRoutes.js";
// import appointmentRoute from "./routes/appointmentRoutes.js";
// import notificationRoute from "./routes/notificationRoutes.js";
// import conversationRoute from "./routes/conversationRoute.js";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());
// dot env
dotenv.config();
const PORT = process.env.PORT;
const MongoDBURI = process.env.MONGO_URI;

// middlewares
app.use(morgan("dev"));

// connect mongoDB
connectDb(MongoDBURI);
app.use("/user/api/v1", userRoutes);

app.listen(
  PORT,
  console.log(`Server running in mode on port http://localhost:${PORT}`)
);
