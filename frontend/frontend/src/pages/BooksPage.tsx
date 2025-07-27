// pages/BooksPage.tsx
import LogoutButton from '../components/LogoutButton';

export default function BooksPage() {
  return (
    <div>
      <div className="header">
        <h1>Book Inventory</h1>
        <LogoutButton />
      </div>
      {/* Your book table component */}
    </div>
  );
}