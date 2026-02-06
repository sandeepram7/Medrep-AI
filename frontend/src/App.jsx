import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ChatPage from "./pages/ChatPage";
import DrugExplorer from "./pages/DrugExplorer";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<ChatPage />} />
        <Route path="/drugs" element={<DrugExplorer />} />
      </Route>
    </Routes>
  );
}
