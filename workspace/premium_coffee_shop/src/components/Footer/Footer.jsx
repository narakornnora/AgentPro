import React from 'react';
import { cn } from '@/lib/utils';

interface FooterProps {
  className?: string;
  children?: React.ReactNode;
}

export const Footer: React.FC<FooterProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div className={cn('', className)} {...props}>
      {Footer Component}
      {children}
    </div>
  );
};

export default Footer;
