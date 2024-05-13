import adminModel from "../models/AdminModel.js";
import asyncHandler from "express-async-handler";
import userModel from "../models/userModel.js";
import Payment from "../models/PaymentModel.js";

const adminLogin = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password)
    return res
      .status(400)
      .json({ message: "Provide complete credentials", success: false });

  const adminExist = await adminModel.findOne({ email: email });
  if (!adminExist)
    return res
      .status(400)
      .json({ message: "No such email exists.", success: false });

  const admin = await adminModel
    .findOne({ email: email, password: password })
    .select("-password");

  if (!admin)
    return res
      .status(400)
      .json({ message: "Incorrect Credentials.", success: false });

  return res
    .status(200)
    .json({ message: "Logged In Successfully", data: admin, success: true });
});

const userList = asyncHandler(async (req, res) => {
  const { adminId } = req.body;
  if (!adminId)
    return res
      .status(400)
      .json({ message: "Provide complete credentials", success: false });
  const admin = await adminModel.findOne({ _id: adminId });
  if (!admin)
    return res
      .status(400)
      .json({ message: "Not allowed to access.", success: false });
  const user = await userModel
    .find()
    .select("-password")
    .sort({ createdAt: -1 });
  return res.status(200).json({
    message: "User List Sent Successfully",
    data: user,
    success: true,
  });
});

const userDelete = asyncHandler(async (req, res) => {
  const { adminId, userId } = req.body;
  if (!adminId || !userId)
    return res
      .status(400)
      .json({ message: "Provide complete credentials", success: false });
  const admin = await adminModel.findOne({ _id: adminId });
  if (!admin)
    return res
      .status(400)
      .json({ message: "Not allowed to access.", success: false });
  const user = await userModel.findById(userId);
  if (!user)
    return res
      .status(400)
      .json({ message: "User doesn;t exists.", success: false });
  await userModel.findByIdAndDelete(userId);
  return res.status(200).json({
    message: "User Deleted Successfully",
    success: true,
  });
});

const paymentList = asyncHandler(async (req, res) => {
  try {
    const { adminId } = req.body;
    if (!adminId)
      return res
        .status(400)
        .json({ message: "Provide complete credentials", success: false });
    const admin = await adminModel.findOne({ _id: adminId });
    if (!admin)
      return res
        .status(400)
        .json({ message: "Not allowed to access.", success: false });
    const payment = await Payment.find()
      .select("userId totalAmount razorpayPaymentId paymentStatus updatedAt")
      .populate({
        path: "userId",
        select: "name email phone",
      })
      .sort({ createdAt: -1 });
    if (!payment)
      return res
        .status(400)
        .json({ message: "No payments found", success: false });
    return res.status(200).json({
      message: "Payment List Sent Successfully",
      data: payment,
      success: true,
    });
  } catch (error) {
    console.log(error);
  }
});

export { adminLogin, userList, userDelete, paymentList };
