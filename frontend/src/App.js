import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { Car, RefreshCw, MapPin, Clock, TrendingUp, Users, Activity } from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [parkingData, setParkingData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [parkingResponse, summaryResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/api/parking`),
        axios.get(`${API_BASE_URL}/api/parking/summary`)
      ]);
      
      setParkingData(parkingResponse.data);
      setSummary(summaryResponse.data);
      setLastUpdated(new Date());
    } catch (err) {
      setError('Unable to fetch parking data. Please try again later.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 3 minutes
    const interval = setInterval(fetchData, 180000);
    return () => clearInterval(interval);
  }, []);

  const getOccupationColor = (occupation) => {
    if (occupation < 30) return '#10b981'; // green
    if (occupation < 70) return '#f59e0b'; // orange
    return '#ef4444'; // red
  };

  const getOccupationStatus = (occupation) => {
    if (occupation < 30) return 'Low';
    if (occupation < 70) return 'Medium';
    return 'High';
  };

  if (loading && parkingData.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
        <div className="text-white text-center">
          <RefreshCw className="animate-spin mx-auto mb-4" size={48} />
          <p className="text-xl">Loading parking data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4 bg-gradient-to-br from-blue-500 to-purple-600">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="glass-effect rounded-xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Car className="text-white" size={32} />
              <div>
                <h1 className="text-3xl font-bold text-white">Vigo Parking Monitor</h1>
                <p className="text-white/80">Real-time parking occupation data</p>
              </div>
            </div>
            <button
              onClick={fetchData}
              disabled={loading}
              className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={loading ? 'animate-spin' : ''} size={20} />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/20 border border-red-500/50 text-white p-4 rounded-lg mb-6">
            <p>{error}</p>
          </div>
        )}

        {/* Summary Cards */}
        {summary && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div className="glass-effect rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm">Total Parking Lots</p>
                  <p className="text-2xl font-bold text-white">{summary.total_parking_lots}</p>
                </div>
                <MapPin className="text-white/60" size={24} />
              </div>
            </div>

            <div className="glass-effect rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm">Total Spaces</p>
                  <p className="text-2xl font-bold text-white">{summary.total_spaces.toLocaleString()}</p>
                </div>
                <Users className="text-white/60" size={24} />
              </div>
            </div>

            <div className="glass-effect rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm">Free Spaces</p>
                  <p className="text-2xl font-bold text-white">{summary.free_spaces.toLocaleString()}</p>
                </div>
                <Activity className="text-white/60" size={24} />
              </div>
            </div>

            <div className="glass-effect rounded-xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-white/80 text-sm">Average Occupation</p>
                  <p className="text-2xl font-bold text-white">{summary.avg_occupation.toFixed(1)}%</p>
                </div>
                <TrendingUp className="text-white/60" size={24} />
              </div>
            </div>
          </div>
        )}

        {/* Simple Table */}
        <div className="glass-effect rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">📋 Parking Information</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-white">
              <thead>
                <tr className="border-b border-white/20">
                  <th className="text-left py-2 px-2">Parking</th>
                  <th className="text-center py-2 px-2">Free</th>
                  <th className="text-center py-2 px-2">Total</th>
                  <th className="text-center py-2 px-2">Occ.</th>
                  <th className="text-center py-2 px-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {parkingData
                  .sort((a, b) => b.ocupacion - a.ocupacion)
                  .map((parking) => (
                    <tr key={parking.nombre} className="border-b border-white/10 hover:bg-white/10">
                      <td className="py-2 px-2 text-sm">{parking.nombre}</td>
                      <td className="text-center py-2 px-2 text-sm">{parking.plazaslibres}</td>
                      <td className="text-center py-2 px-2 text-sm">{parking.totalplazas}</td>
                      <td className="text-center py-2 px-2 text-sm">{parking.ocupacion}%</td>
                      <td className="text-center py-2 px-2">
                        <span
                          className="px-2 py-1 rounded-full text-xs font-medium"
                          style={{
                            backgroundColor: getOccupationColor(parking.ocupacion) + '20',
                            color: getOccupationColor(parking.ocupacion),
                            border: `1px solid ${getOccupationColor(parking.ocupacion)}`
                          }}
                        >
                          {getOccupationStatus(parking.ocupacion)}
                        </span>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer */}
        <div className="glass-effect rounded-xl p-4 mt-6 text-center">
          <div className="flex items-center justify-center space-x-4 text-white/80 text-sm">
            <div className="flex items-center space-x-1">
              <Clock size={16} />
              <span>Last updated: {lastUpdated ? lastUpdated.toLocaleString() : 'Never'}</span>
            </div>
            <span>•</span>
            <span>Data source: Vigo City Council Open Data</span>
            <span>•</span>
            <span>Auto-refresh every 3 minutes</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
