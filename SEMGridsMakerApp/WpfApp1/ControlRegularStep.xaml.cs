using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace SEMGridsMakerApp
{
    /// <summary>
    /// Logique d'interaction pour ControlRegularStep.xaml
    /// </summary>
    public partial class ControlRegularStep : UserControl
    {
        public ControlRegularStep()
        {
            InitializeComponent();
        }

        

        private void Button_Menu_Click(object sender, RoutedEventArgs e)
        {
            ((ContentControl)this.Parent).Content = new ControlMenu();
        }
    }
}
