import { Outlet } from 'react-router-dom';

export function AuthLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-700 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-2xl shadow-lg mb-4">
            <span className="text-blue-900 font-bold text-2xl">D</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Doctor Data Platform</h1>
          <p className="text-blue-200 text-sm mt-1">Your trusted medical directory</p>
        </div>

        {/* Auth Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <Outlet />
        </div>

        <p className="text-center text-blue-200 text-xs mt-6">
          © 2024 Doctor Data Platform. All rights reserved.
        </p>
      </div>
    </div>
  );
}
