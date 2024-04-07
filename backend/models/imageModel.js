import mongoose from "mongoose";

const userSchema = new mongoose.Schema({
  user: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "users",
    require: true,
  },
  url: {
    type: String,
    required: [true, "URL is required"],
  },
});

const imageModel = mongoose.model("image", userSchema);

export default imageModel;
