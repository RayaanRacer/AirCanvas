import mongoose from "mongoose";

// payment
const PaymentSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "users",
      required: true,
    },
    paymentDate: {
      type: String,
      trim: true,
    },
    totalAmount: {
      type: Number,
    },
    amountPaid: {
      type: Number,
    },
    razorpayOrderId: {
      type: String,
      trim: true,
    },
    razorpayPaymentId: {
      type: String,
      trim: true,
    },
    razorpaySignature: {
      type: String,
      trim: true,
    },
    paymentStatus: {
      type: String,
      enum: ["Pending", "Fully Paid", "Partially Paid"],
      default: "Pending",
    },
  },
  { timestamps: true }
);

const Payment = mongoose.model("Payment", PaymentSchema);
export default Payment;
