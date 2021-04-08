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
    /// Logique d'interaction pour ControlMenu.xaml
    /// </summary>
    public partial class ControlMenu : UserControl
    {
        public ControlMenu()
        {
            InitializeComponent();
        }

        private void Button_RegularStep_Click(object sender, RoutedEventArgs e)
        {
            ContentControlMenu.Content = new ControlRegularStep();
        }
    }
}
