import React from "react";
import { Phone, MessageCircle } from "lucide-react";

export default function NssiLandWebsite() {
  return (
    <div className="min-h-screen bg-gray-100 text-gray-800">

      {/* Header */}
      <header className="bg-green-700 text-white p-5 text-center text-2xl font-bold rounded-b-2xl shadow">
        NSSI Land Promoters - Calicut
      </header>

      {/* Hero Section */}
      <section className="p-6 text-center">
        <h1 className="text-3xl font-bold mb-3">
          Buy & Sell Properties Easily 🏡
        </h1>
        <p className="mb-4">
          Fast deals | Genuine buyers | Full marketing support
        </p>

        <div className="flex justify-center gap-4">
          <button className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-xl flex items-center">
            <Phone className="mr-2" /> Call Now
          </button>

          <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center">
            <MessageCircle className="mr-2" /> WhatsApp
          </button>
        </div>
      </section>

      {/* Services */}
      <section className="p-6 grid md:grid-cols-3 gap-4">
        {["Property Buying", "Property Selling", "Marketing Support"].map(
          (service, i) => (
            <div key={i} className="bg-white p-4 rounded-2xl shadow text-center font-semibold">
              {service}
            </div>
          )
        )}
      </section>

      {/* About */}
      <section className="p-6 text-center">
        <h2 className="text-xl font-bold mb-2">About Us</h2>
        <p>
          NSSI Land Promoters is a trusted property marketing company in Calicut.
          We help clients buy and sell land quickly with genuine customers and full support.
        </p>
      </section>

      {/* Contact */}
      <section className="p-6 text-center">
        <h2 className="text-xl font-bold mb-2">Contact Us</h2>
        <p className="mb-2">Phone / WhatsApp: 8590304889</p>

        <button className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-xl">
          Contact Now
        </button>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center p-4 mt-6">
        © 2026 NSSI Land Promoters. All rights reserved.
      </footer>
    </div>
  );
}
