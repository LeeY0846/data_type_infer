import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css'
import Root from './router/root';
import FilePage, { loader as fileListLoader } from './router/filePage';
import { action as deleteFileAction } from './router/deleteFIle';
import TablePage, { loader as tableLoader } from './router/table';


const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    children: [
      {
        index: true,
        loader: fileListLoader,
        element: <FilePage />,
      },
      {
        path: "/:fileID/delete",
        action: deleteFileAction,
      },
      {
        path:"/table/:fileID",
        loader: tableLoader,
        element: <TablePage />,
      }
    ],
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
