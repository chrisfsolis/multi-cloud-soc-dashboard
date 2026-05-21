interface CardProps {
  title?: string;
  children: React.ReactNode;
  className?: string;
  action?: React.ReactNode;
}

export default function Card({ title, children, className = "", action }: CardProps) {
  return (
    <div className={`bg-slate-800 border border-slate-700 rounded-xl ${className}`}>
      {(title || action) && (
        <div className="flex items-center justify-between px-5 py-3 border-b border-slate-700">
          {title && (
            <h3 className="text-sm font-semibold text-white">{title}</h3>
          )}
          {action}
        </div>
      )}
      <div className="p-5">{children}</div>
    </div>
  );
}
